import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os.path

"""
-----------------------------------------------------------------------------------------------------

Foreword:

This code was created as a personal project for the further improvement of WestRock's Packaging Machinery & Automation (PMA) division. The overall purporse of this is to take two BOMs
(one from Inventor, one from IFS) and compare them, returning a list of differences including differences in composition (for example, if a part number was found in Inventor but not IFS and vice versa) as well as 
differences in quantity (for example, if IFS said there were 3 of part 12345 while Inventor said there were 2 of that part). The goal is to help quell the issue stated above, decreasing error across BOMs and easily
identifying any errors if one is to arise. This will decrease production time, decrease errors, and decrease the amount of troubleshooting and painstaking line-by-line comparison on the engineering side when such
an issue arrives.

For reference, this code was created with help from a variety of sources. Due to my lack of prior experience with Tkinter, a lot of helpful information was found at tkdocs.com/tutorial, including the use of some 
prior-developed code in the tutorial. Furthermore, a few of my questions were answered via StackOverflow browsing, and several other forums helped fill in the gaps where necessary.

If you ever need revision on this code, feel free to update it as need be. Hopefully my documentation is thorough enough to make sense of each individual code block. If any questions arise, I have found these following
sources to be incredibly beneficial in the development of this program:

https://tkdocs.com/tutorial/index.html
https://docs.python.org/3/library/dialog.html
https://stackoverflow.com/questions/16923281/writing-a-pandas-dataframe-to-csv-file

Should any more questions arise, you can reach me at kev.connell.22@gmail.com. Best of luck.

-----------------------------------------------------------------------------------------------------
"""

# Creates the dataframe for each particular document, both the Inventor and IFS CSVs.
def inv_file_to_list():
    global inventor_pn
    global inventor_qty
    global inv_file_name
    filepath = filedialog.askopenfilename()
    inv_file_name = filepath
    file = open(filepath,'r')
    dI = pd.read_csv(file, usecols=['Part Number', 'Description', 'QTY'])
    inventor_pn = dI["Part Number"].values.tolist()
    inventor_qty = dI["QTY"].values.tolist()

    inv_filename.set(filepath)

#Creates the dataframe from the IFS document, accepting a filepath as an argument
def ifs_file_to_list():
    global ifs_pn
    global ifs_qty
    filepath = filedialog.askopenfilename()
    file = open(filepath,'r')
    dIFS = pd.read_csv(file, usecols=['Part Number', 'Part Description', 'Quantity  Per Assembly'])
    ifs_pn = dIFS["Part Number"].values.tolist()
    ifs_qty = dIFS["Quantity  Per Assembly"].values.tolist()

    ifs_filename.set(filepath)

# Function for the process of removing leading zeroes from the Inventor BOM
#DELETE if IFS can be downloaded while keeping leading zeroes!!!
def remove_leading_zeros(list_characters):
    while True:
        if list_characters[0] == "0":
            del list_characters[0]
        else:
            break


# Function for the purging of different lists [See create_dif_list for use]
def purge_list(list1, list2, list3):
    for item in list1:
        for i in range(len(list2)):
            if i == item:
                list3.append(list2[i])


# Creates the list of correct pn's, but different quantities (returns list of part number and quantity in both Inventor and IFS)
# Looks bad, but is fully functional. Returns list of lists, giving PN, Qty in Inv, and IFS QTY
def create_dif_list():
    
    inv_qty_idx = []
    ifs_qty_idx = []
    # Removes leading zeros from the inventor part number list
    for i in range(len(inventor_pn)):
        number_list = list(inventor_pn[i])
        remove_leading_zeros(number_list)
        new_number = ''.join(number_list)
        inventor_pn[i] = new_number

    common = set(inventor_pn).intersection(set(ifs_pn))

    # Two sets of code that copy over indicies of matching part numbers over...very helpful
    for item in common:
        for i in range(len(inventor_pn)):
            if inventor_pn[i] == item:
                inv_qty_idx.append(i)
    for item in common:
        for i in range(len(ifs_pn)):
            if ifs_pn[i] == item:
                ifs_qty_idx.append(i)

    # Creates empty lists for storage of only common parts (found in next set of code using purge_list)
    inv_pn_final = []
    inv_qty_final = []
    ifs_pn_final = []
    ifs_qty_final = []

    # Purges all lists (PN and QTY) of unique values, leaving only common ones behind
    purge_list(inv_qty_idx, inventor_pn, inv_pn_final)
    purge_list(inv_qty_idx, inventor_qty, inv_qty_final)
    purge_list(ifs_qty_idx, ifs_pn, ifs_pn_final)
    purge_list(ifs_qty_idx, ifs_qty, ifs_qty_final)

    # Creates master list of tuples containing part number and qty for each common part
    inv_master = []
    for i in range(len(inv_pn_final)):
        inv_master.append((inv_pn_final[i], inv_qty_final[i]))
    ifs_master = []
    for i in range(len(ifs_pn_final)):
        ifs_master.append((ifs_pn_final[i], ifs_qty_final[i]))

    list_differences = []

    # If the part number is the same but the quantities differ, then the whole list (part number, qty in Inv, qty in IFS) is appended to the list of differences
    for i in range(len(inv_master)):
        for j in range(len(ifs_master)):
            if inv_master[i][0] == ifs_master[j][0] and inv_master[i][1] != ifs_master[j][1]:
                list_differences.append([inv_master[i][0], inv_master[i][1], ifs_master[j][1]])

    return list_differences

# Function ONLY comparing the two CSVs (does NOT export)
def compare():
    # Creates the list of quantity differences using create_dif_list given the file names
    list_qty_dif = create_dif_list()
    for i in range(len(list_qty_dif)):
        list_qty_dif[i] = [list_qty_dif[i][0], "Y", "Y", list_qty_dif[i][1], list_qty_dif[i][2]]
      
    # Removes leading zeroes from the inventor part number list
    for i in range(len(inventor_pn)):
        number_list = list(inventor_pn[i])
        remove_leading_zeros(number_list)
        new_number = ''.join(number_list)
        inventor_pn[i] = new_number

    # This code block creates lists of indexes where part numbers match
    inv_idx_list = []
    ifs_idx_list = []

    for i in range(len(inventor_pn)):
        for j in range(len(ifs_pn)):
            if inventor_pn[i] == ifs_pn[j]:
                inv_idx_list.append(i)
                ifs_idx_list.append(j)

    # Code block replaces common part numbers found in Inventor with "?", then appends all numbers that are not "?" to inv_masterpart of a list including the quantity and presence in Inventor/IFS
    inv_master = []
    ifs_master = []

    for i in range(len(inventor_pn)):
        for item in inv_idx_list:
            if i == item:
                inventor_pn[i] = "?"
    for i in range(len(inventor_pn)):
        if inventor_pn[i] != "?":
            inv_master.append([inventor_pn[i], "Y", "N", inventor_qty[i], 0])

    # Code block replaces common part numbers found in IFS with "&", then appends all numbers thht are not "&" to ifs_master as part of a list including the quantity and presence in Inventor/IFS
    for i in range(len(ifs_pn)):
        for item in ifs_idx_list:
            if i == item:
                ifs_pn[i] = "&"
    for i in range(len(ifs_pn)):
        if ifs_pn[i] != "&":
            ifs_master.append([ifs_pn[i], "N", "Y", 0, ifs_qty[i]])

    # Creates dataframes from the inv_master, ifs_master, and the quantity differences list "qty" to represent Part Number, Found in Inventor/IFS, and quantities in both
    inventor_df = pd.DataFrame(inv_master,
                               columns=['Part Number', 'In Inventor?', 'In IFS?', 'Inventor Quantity', 'IFS Quantity'])
    ifs_df = pd.DataFrame(ifs_master,
                          columns=['Part Number', 'In Inventor?', 'In IFS?', 'Inventor Quantity', 'IFS Quantity'])
    qty_df = pd.DataFrame(list_qty_dif,
                          columns=['Part Number', 'In Inventor?', 'In IFS?', 'Inventor Quantity', 'IFS Quantity'])

    # Creates a final dataframe by concatenating each individual dataframe above into a final dataframe
    comparison_csv_df = [inventor_df, ifs_df, qty_df]
    comparison_final = pd.concat(comparison_csv_df)

    # Divides the final dataframe along column lines, helping to make the final output more readable in the GUI
    pn = comparison_final[['Part Number']].to_string(index=False)
    inv = comparison_final[['In Inventor?']].to_string(index=False)
    ifs = comparison_final[['In IFS?']].to_string(index=False)
    inv_q = comparison_final[['Inventor Quantity']].to_string(index=False)
    ifs_q = comparison_final[['IFS Quantity']].to_string(index=False)

    # Sets the GUI space to display each individual dataframe column
    number.set(pn)
    inventor.set(inv)
    ifs_internal.set(ifs)
    inventor_q.set(inv_q)
    ifs_internal_q.set(ifs_q)


# This function compares the CSVs and exports results to a new CSV file
def export():
    # Creates the list of quantity differences using create_dif_list given the file names
    list_qty_dif = create_dif_list()
    for i in range(len(list_qty_dif)):
        list_qty_dif[i] = [list_qty_dif[i][0], "Y", "Y", list_qty_dif[i][1], list_qty_dif[i][2]]

    # Removes leading zeroes from the inventor part number list
    for i in range(len(inventor_pn)):
        number_list = list(inventor_pn[i])
        remove_leading_zeros(number_list)
        new_number = ''.join(number_list)
        inventor_pn[i] = new_number

    # This code block creates lists of indexes where part numbers match
    inv_idx_list = []
    ifs_idx_list = []

    for i in range(len(inventor_pn)):
        for j in range(len(ifs_pn)):
            if inventor_pn[i] == ifs_pn[j]:
                inv_idx_list.append(i)
                ifs_idx_list.append(j)

    # Code block replaces common part numbers found in Inventor with "?", then appends all numbers that are not "?" to inv_masterpart of a list including the quantity and presence in Inventor/IFS
    inv_master = []
    ifs_master = []
  
    for i in range(len(inventor_pn)):
        for item in inv_idx_list:
            if i == item:
                inventor_pn[i] = "?"
    for i in range(len(inventor_pn)):
        if inventor_pn[i] != "?":
            inv_master.append([inventor_pn[i], "Y", "N", inventor_qty[i], 0])

    # Code block replaces common part numbers found in IFS with "&", then appends all numbers thht are not "&" to ifs_master as part of a list including the quantity and presence in Inventor/IFS
    for i in range(len(ifs_pn)):
        for item in ifs_idx_list:
            if i == item:
                ifs_pn[i] = "&"
    for i in range(len(ifs_pn)):
        if ifs_pn[i] != "&":
            ifs_master.append([ifs_pn[i], "N", "Y", 0, ifs_qty[i]])

    # Creates dataframes from the inv_master, ifs_master, and the quantity differences list "qty" to represent Part Number, Found in Inventor/IFS, and quantities in both
    inventor_df = pd.DataFrame(inv_master,
                               columns=['Part Number', 'In Inventor?', 'In IFS?', 'Inventor Quantity', 'IFS Quantity'])
    ifs_df = pd.DataFrame(ifs_master,
                          columns=['Part Number', 'In Inventor?', 'In IFS?', 'Inventor Quantity', 'IFS Quantity'])
    qty_df = pd.DataFrame(list_qty_dif,
                          columns=['Part Number', 'In Inventor?', 'In IFS?', 'Inventor Quantity', 'IFS Quantity'])

    # Creates a final dataframe by concatenating each individual dataframe above into a final dataframe
    comparison_csv_df = [inventor_df, ifs_df, qty_df]
    comparison_final = pd.concat(comparison_csv_df)

    # Divides the final dataframe along column lines, helping to make the final output more readable in the GUI
    pn = comparison_final[['Part Number']].to_string(index=False)
    inv = comparison_final[['In Inventor?']].to_string(index=False)
    ifs = comparison_final[['In IFS?']].to_string(index=False)
    inv_q = comparison_final[['Inventor Quantity']].to_string(index=False)
    ifs_q = comparison_final[['IFS Quantity']].to_string(index=False)

    # Sets the save path directory for the new CSV results file
    save_path = filedialog.askdirectory()
    os.chdir(f'{save_path}')
    comparison_final.to_csv("BOM Comparison Results.csv", encoding='utf-8', index=False)
    completion.set("Done!")

    # Sets the GUI space to display each individual dataframe column
    number.set(pn)
    inventor.set(inv)
    ifs_internal.set(ifs)
    inventor_q.set(inv_q)
    ifs_internal_q.set(ifs_q)

# Function that resets the entire program, deleting the data in order to allow for new input CSVs
def clear():
    # Clears inventor/ifs specific lists
    global inventor_pn
    global ifs_pn
    global inventor_qty
    global ifs_qty
    inventor_pn = []
    ifs_pn = []
    inventor_qty = []
    ifs_qty = []

    # Clears inventor/ifs/qty dataframes
    global inventor_df
    global ifs_df
    global qty_df
    inventor_df = []
    ifs_df = []
    qty_df = []

    # Clears results that are present in GUI
    number.set("")
    inventor.set("")
    ifs_internal.set("")
    inventor_q.set("")
    ifs_internal_q.set("")

    # Clears previous file name and directory information, letting user choose new files
    inv_filename.set("")
    ifs_filename.set("")
    completion.set("")


# Creates the GUI base using Tkinter
root = Tk()
root.title("Inventor v. IFS BOM Comparison")

# Sets basic mainframe grid to be used in initial screen
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Creates the "WARNING" text at the bottom, instructing user to reset the GUI after every single iteration to ensure accurate results
ttk.Label(mainframe, text="WARNING: You MUST click 'Reset' after every single comparison test, even if you want to do Quick Compare and then Compare/Export.").grid(column=3, row=11, sticky=N)

# Creates the input button for the Inventor filepath
inv_filename_entry = ttk.Button(mainframe, text="Select File", command=inv_file_to_list)
inv_filename_entry.grid(column=3, row=3, sticky=(W, E))

# Creates the input button for the IFS filepath
ifs_filename_entry = ttk.Button(mainframe, text="Select File", command=ifs_file_to_list)
ifs_filename_entry.grid(column=3, row=6, sticky=(W, E))
#inv_filename_entry = ttk.Entry(mainframe, width=12, textvariable=ifs_filename)

# Creates directory name displays in the GUI
inv_filename = StringVar()
ifs_filename = StringVar()
ttk.Label(mainframe, textvariable=inv_filename).grid(column=3, row=2, sticky=N)
ttk.Label(mainframe, textvariable=ifs_filename).grid(column=3, row=5, sticky=N)

# Creates the submit button (I hate this button.)
ttk.Button(mainframe, text="Quick Compare (Display Only)", command=compare).grid(column=3, row=7, sticky=N)

# Creates the labels for IFS and Inventor filename submission boxes
ttk.Label(mainframe, text="Inventor BOM Filename: ").grid(column=3, row=1, sticky=N)
ttk.Label(mainframe, text="IFS BOM Filename: ").grid(column=3, row=4, sticky=N)

# Creates the completion status label next to the "Export" button
completion = StringVar()
ttk.Label(mainframe, textvariable=completion).grid(column=4,row=8,sticky=(N, W))

# Creates the variables where the output dataframes will be displayed
number = StringVar()
inventor = StringVar()
ifs_internal = StringVar()
inventor_q = StringVar()
ifs_internal_q = StringVar()

# Creates final output display areas on GUI
ttk.Label(mainframe, textvariable=number).grid(column=1, row=9, sticky=E)
ttk.Label(mainframe, textvariable=inventor).grid(column=2, row=9, sticky=E)
ttk.Label(mainframe, textvariable=ifs_internal).grid(column=3, row=9, sticky=N)
ttk.Label(mainframe, textvariable=inventor_q).grid(column=4, row=9, sticky=W)
ttk.Label(mainframe, textvariable=ifs_internal_q).grid(column=5, row=9, sticky=W)

# Creates button for the "Compare/Export" feature
ttk.Button(mainframe, text="Compare/Export to CSV", command=export).grid(column=3, row=8, sticky=N)

# Creates button for the "Clear" feature
ttk.Button(mainframe, text="Reset", command=clear).grid(column=3,row=10,sticky=N)

# Added padding around each element in the grid for visual purposes
for child in mainframe.winfo_children():
    child.grid_configure(padx=10, pady=10)

# Binds "enter" to "Quick Compare" button
root.bind("<Return>", compare)

# Runs the tkinter program to keep window open
root.mainloop()
