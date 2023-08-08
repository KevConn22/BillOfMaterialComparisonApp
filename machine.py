# Library imports necessary for code
import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os.path

"""

-------------------------------------------------------------------------------------------------------------
What's up!

It's me again, this time trying something that's probably going to be more difficult. Instead of simply running a per-basis comparison, I am instead going to be doing a whole-machine comparison.

Good luck, and let's see the code!
-------------------------------------------------------------------------------------------------------------
Assumptions:
In order for this program to work, we have to operate off of a certain set of assumptions. For this one in particular, we are looking at whole-machine parts analysis. That means we have to have the CSV for EVERY SUBASSEMBLY prior to launching and running this program. That is something that will be very difficult, but will still take considerably less time when compared to manually counting all parts of a machine (come on, it'll be very beneficial in that regard). 

Pseudocoding:

abstraction of parts:
    bomlist = []    
    get directory of all file csvs

    for file in directory:
        temp = []
        open file
        read columns "number", "qty" from file
        read data to_list

    
        
    for i in range
        
"""

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
    dIFS = pd.read_csv(file, usecols=['Component Part', 'Component Part Description', 'Qty per Assembly'])
    ifs_pn = dIFS["Component Part"].values.tolist()
    ifs_qty = dIFS["Qty per Assembly"].values.tolist()

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

# Added padding around each element in the grid for visual purposes
for child in mainframe.winfo_children():
    child.grid_configure(padx=10, pady=10)

# Runs the tkinter program to keep window open
root.mainloop()
