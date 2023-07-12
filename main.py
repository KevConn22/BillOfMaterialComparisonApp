import pandas as pd
from tkinter import *
from tkinter import ttk
import csv
import openpyxl

"""
For reference, this code was created with help from a variety of sources. Due to my lack of prior experience with Tkinter, a lot of helpful information was found at tkdocs.com/tutorial, including the use of some prior-developed code in the tutorial. Furthermore, a few of my questions were answered via StackOverflow browsing, and several other forums helped fill in the gaps where necessary.

Psuedocoding:

For each individual column of the CSV:
1. Must iterate through entire column, print to a new CSV for comparison.
2. Must iterate through entire column on IFS CSV, printing to new column of new CSV

Following this, we will have two columns, A and B. For each item, we have to somehow do the following:

Determine the deltas of the columns, then report which one is in IFS vs. Inventor (if they belong to Column A or Column B)

Idea:

For Item in A:
  For Item in B:
    If ItemA == ItemB:
      Print(True)

For Item in B:
  For Item in A:
    If ItemB == ItemA:
      Print(True)

Any values that do not have a "True" designation therefore do not have a match in the other column, making them easy to tag after the fact.
"""
"""root = Tk()
root.title("Inventor/IFS CSV BOM Comparison")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
"""
#Creates the dataframe for each particular document, both the Inventor and IFS CSVs.
def create_inv_list(filename):
  dI = pd.read_csv(filename, usecols=['Part Number', 'Description', 'QTY'])
  inventor_pn = dI["Part Number"].values.tolist()
  inventor_qty = dI["QTY"].values.tolist()
  return inventor_pn

def inv_qty_list(filename):
  dI = pd.read_csv(filename, usecols=['Part Number', 'Description', 'QTY'])
  inventor_qty = dI["QTY"].values.tolist()
  return inventor_qty
  
def create_ifs_list(filename):
  dIFS = pd.read_csv(filename, usecols=['Part Number', 'Part Description', 'Quantity  Per Assembly'])
  ifs_pn = dIFS["Part Number"].values.tolist()
  ifs_qty = dIFS["Quantity  Per Assembly"].values.tolist()
  return ifs_pn

def ifs_qty_list(filename):
  dIFS = pd.read_csv(filename, usecols=['Part Number', 'Part Description', 'Quantity  Per Assembly'])
  ifs_qty = dIFS["Quantity  Per Assembly"].values.tolist()
  return ifs_qty

#Function for the process of removing zeroes
def remove_leading_zeros(list_characters):
  while True:
    if list_characters[0] == "0":
      del list_characters[0]
    else:
      break

#Function for the purging of different lists [See create_dif_list for use]
def purge_list(list1, list2, list3):
  for item in list1:
    for i in range(len(list2)):
      if i == item:
        list3.append(list2[i])
        
#Creates the list of correct pn's, but different quantities (returns list of part number and quantity in both Inventor and IFS)
#Looks bad, but is fully functional. Returns list of lists, giving PN, Qty in Inv, and IFS QTY
def create_dif_list(f1, f2):
  inv_qty_idx = []
  ifs_qty_idx = []
  
  #Note for any future reference: if you are coming up with errors after switching, check these categories. It might be that the names for the categories changed (while these are the current standards for Inv/IFS, they might change.) Simply update them here and elsewhere throughout the code and it should continue to run.
  dI= pd.read_csv(f1, usecols=['Part Number', 'Description', 'QTY'])
  dIFS = pd.read_csv(f2, usecols=['Part Number', 'Part Description', 'Quantity  Per Assembly'])
  
  inventor_pn = dI["Part Number"].values.tolist()
  inventor_qty = dI["QTY"].values.tolist()
  ifs_pn = dIFS["Part Number"].values.tolist()
  ifs_qty = dIFS["Quantity  Per Assembly"].values.tolist()
  for i in range(len(inventor_pn)):
    number_list = list(inventor_pn[i])
    remove_leading_zeros(number_list)
    new_number = ''.join(number_list)
    inventor_pn[i] = new_number
  common = set(inventor_pn).intersection(set(ifs_pn))
  
  #Two sets of code that copy over indicies of matching part numbers over...very helpful
  for item in common:
    for i in range(len(inventor_pn)):
      if inventor_pn[i] == item:
        inv_qty_idx.append(i)
  for item in common:
    for i in range(len(ifs_pn)):
      if ifs_pn[i] == item:
        ifs_qty_idx.append(i)

  #Creates the list of only those part numbers and quantities
  inv_pn_final = []
  inv_qty_final = []
  ifs_pn_final = []
  ifs_qty_final = []  

  #Purges all lists (PN and QTY) of unique values, leaving only common ones behind
  purge_list(inv_qty_idx, inventor_pn, inv_pn_final)
  purge_list(inv_qty_idx, inventor_qty, inv_qty_final)
  purge_list(ifs_qty_idx, ifs_pn, ifs_pn_final)
  purge_list(ifs_qty_idx, ifs_qty, ifs_qty_final)

  #Creates master list of tuples containing part number and qty for each common part
  inv_master = []
  for i in range(len(inv_pn_final)):
    inv_master.append((inv_pn_final[i], inv_qty_final[i]))
  ifs_master = []
  for i in range(len(ifs_pn_final)):
    ifs_master.append((ifs_pn_final[i], ifs_qty_final[i]))

  list_differences = []
  
  for i in range(len(inv_master)):
    for j in range(len(ifs_master)):
      if inv_master[i][0] == ifs_master[j][0] and inv_master[i][1] != ifs_master[j][1]:
        list_differences.append([inv_master[i][0], inv_master[i][1], ifs_master[j][1]])

  return list_differences
  
#Removes leading zeros from inventor_pn list (CSV from IFS does so, so must do so here)
#OBSELETE as of 7/10/23; implemented directly into "compare" function
def update_list_removed_zeros():
  for i in range(len(inv_list)):
    number_list = list(inv_list[i])
    remove_leading_zeros(number_list)
    new_number = ''.join(number_list)
    inv_list[i] = new_number

#Function for overall comparison, taking into account all functions listed above
#FUNCTION WORKS WHEN PASSED BOTH PARAMETERS AS STRINGS
def compare(*args):
  inv_name = str(inv_filename.get() + ".csv")
  ifs_name = str(ifs_filename.get() + ".csv")
  
  inv_list = create_inv_list(inv_filename.get() + ".csv")
  ifs_list = create_ifs_list(ifs_filename.get() + ".csv")
  
  list_qty_dif = create_dif_list(inv_name, ifs_name)
  for i in range(len(list_qty_dif)):
    list_qty_dif[i] = [list_qty_dif[i][0], "Y", "Y", list_qty_dif[i][1], list_qty_dif[i][2]]
  inv_qty = inv_qty_list(inv_filename.get() + ".csv")
  ifs_qty = ifs_qty_list(ifs_filename.get() + ".csv")
  
  for i in range(len(inv_list)):
    number_list = list(inv_list[i])
    remove_leading_zeros(number_list)
    new_number = ''.join(number_list)
    inv_list[i] = new_number
  #common = set(inv_list).intersection(set(ifs_list))
  
  inv_idx_list = []
  ifs_idx_list = []
  
  for i in range(len(inv_list)):
    for j in range(len(ifs_list)):
      if inv_list[i] == ifs_list[j]:
        inv_idx_list.append(i)
        ifs_idx_list.append(j)
  
  inv_master = []
  ifs_master = []
  
  for i in range(len(inv_list)):
    for item in inv_idx_list:
      if i == item:
        inv_list[i] = "?"
  for i in range(len(inv_list)):
    if inv_list[i] != "?":
      inv_master.append([inv_list[i], "Y", "N", inv_qty[i], 0])

  for i in range(len(ifs_list)):
    for item in ifs_idx_list:
      if i == item:
        ifs_list[i] = "&"
  for i in range(len(ifs_list)):
    if ifs_list[i] != "&":
      ifs_master.append([ifs_list[i], "N", "Y", 0, ifs_qty[i]])
  
  inventor_df = pd.DataFrame(inv_master, columns=['Part Number', 'In Inventor?', 'In IFS?', 'Inventor Quantity', 'IFS Quantity'])
  ifs_df = pd.DataFrame(ifs_master, columns=['Part Number', 'In Inventor?', 'In IFS?', 'Inventor Quantity', 'IFS Quantity'])
  qty_df = pd.DataFrame(list_qty_dif, columns=['Part Number', 'In Inventor?', 'In IFS?', 'Inventor Quantity', 'IFS Quantity'])
  #inventor.set(inventor_df)
  comparison_csv_df = [inventor_df, ifs_df, qty_df]
  comparison_final = pd.concat(comparison_csv_df)

  pn = comparison_final[['Part Number']].to_string(index=False)
  inv = comparison_final[['In Inventor?']].to_string(index=False)
  ifs = comparison_final[['In IFS?']].to_string(index=False)
  inv_q = comparison_final[['Inventor Quantity']].to_string(index=False)
  ifs_q = comparison_final[['IFS Quantity']].to_string(index=False)

  number.set(pn)
  inventor.set(inv)
  ifs_internal.set(ifs)
  inventor_q.set(inv_q)
  ifs_internal_q.set(ifs_q)

#Function that handles the comparison and subsequent export of the p/n and qty data
def export(*args):
  #Copy of code from compare in order to properly pass the information to the comparison list/dataframe
  inv_name = str(inv_filename.get() + ".csv")
  ifs_name = str(ifs_filename.get() + ".csv")
  
  inv_list = create_inv_list(inv_filename.get() + ".csv")
  ifs_list = create_ifs_list(ifs_filename.get() + ".csv")
  
  list_qty_dif = create_dif_list(inv_name, ifs_name)
  for i in range(len(list_qty_dif)):
    list_qty_dif[i] = [list_qty_dif[i][0], "Y", "Y", list_qty_dif[i][1], list_qty_dif[i][2]]
    
  inv_qty = inv_qty_list(inv_filename.get() + ".csv")
  ifs_qty = ifs_qty_list(ifs_filename.get() + ".csv")
  
  for i in range(len(inv_list)):
    number_list = list(inv_list[i])
    remove_leading_zeros(number_list)
    new_number = ''.join(number_list)
    inv_list[i] = new_number
  #common = set(inv_list).intersection(set(ifs_list))
  
  inv_idx_list = []
  ifs_idx_list = []
  
  for i in range(len(inv_list)):
    for j in range(len(ifs_list)):
      if inv_list[i] == ifs_list[j]:
        inv_idx_list.append(i)
        ifs_idx_list.append(j)
  
  inv_master = []
  ifs_master = []
  
  for i in range(len(inv_list)):
    for item in inv_idx_list:
      if i == item:
        inv_list[i] = "?"
  for i in range(len(inv_list)):
    if inv_list[i] != "?":
      inv_master.append([inv_list[i], "Y", "N", inv_qty[i], 0])

  for i in range(len(ifs_list)):
    for item in ifs_idx_list:
      if i == item:
        ifs_list[i] = "&"
  for i in range(len(ifs_list)):
    if ifs_list[i] != "&":
      ifs_master.append([ifs_list[i], "N", "Y", 0, ifs_qty[i]])
  
  inventor_df = pd.DataFrame(inv_master, columns=['Part Number', 'In Inventor?', 'In IFS?', 'Inventor Quantity', 'IFS Quantity'])
  ifs_df = pd.DataFrame(ifs_master, columns=['Part Number', 'In Inventor?', 'In IFS?', 'Inventor Quantity', 'IFS Quantity'])
  qty_df = pd.DataFrame(list_qty_dif, columns=['Part Number', 'In Inventor?', 'In IFS?', 'Inventor Quantity', 'IFS Quantity'])

  #Codes to write into a CSV file
  comparison_csv_df = [inventor_df, ifs_df, qty_df]
  comparison_final = pd.concat(comparison_csv_df)
  print(comparison_final)
  
  comparison_final.to_csv("BOM Comparison Results.csv", encoding='utf-8', index=False)
  
#Creates the GUI using Tkinter
root = Tk()
root.title("Inventor v. IFS BOM Comparison")

#Sets basic mainframe grid to be used in initial screen
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#Creates the input location for the Inventor filename
inv_filename = StringVar()
inv_filename_entry = ttk.Entry(mainframe, width=12, textvariable=inv_filename)
inv_filename_entry.grid(column=3, row = 2, sticky=(W, E))

#Creates the input location for the IFS filename
ifs_filename = StringVar()
inv_filename_entry = ttk.Entry(mainframe, width=12, textvariable=ifs_filename)
inv_filename_entry.grid(column=3, row=4, sticky=(W, E))

#Creates the submit button (hate this button.)
ttk.Button(mainframe, text="Quick Compare (Enter)", command=compare).grid(column=3, row=5, sticky=N)

#Creates the labels for IFS and Inventor filename submission boxes
ttk.Label(mainframe, text="Inventor BOM Filename: ").grid(column=3, row=1, sticky=N)
ttk.Label(mainframe, text="IFS BOM Filename: ").grid(column=3, row=3, sticky=N)

#Creates final output areas and variables
number = StringVar()
inventor = StringVar()
ifs_internal = StringVar()
inventor_q = StringVar()
ifs_internal_q = StringVar()

ttk.Label(mainframe,textvariable=number).grid(column=1, row=8, sticky=E)
ttk.Label(mainframe,textvariable=inventor).grid(column=2, row=8, sticky=E)
ttk.Label(mainframe,textvariable=ifs_internal).grid(column=3, row=8, sticky=N)
ttk.Label(mainframe,textvariable=inventor_q).grid(column=4, row=8, sticky=W)
ttk.Label(mainframe,textvariable=ifs_internal_q).grid(column=5, row=8, sticky=W)

#Creates button for export to external file
ttk.Button(mainframe, text="Compare/Export to CSV", command=export).grid(column=3, row=6, sticky=N)

#Makes it look more aesthetic by adding padding around each grid element
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=10, pady=10)

#Binds "enter" to "Compare" button
root.bind("<Return>", compare)

#Runs the tkinter program to keep window open
root.mainloop()






#Personal note to Kevin - check out https://stackoverflow.com/questions/66663179/how-to-use-windows-file-explorer-to-select-and-return-a-directory-using-python#:~:text=You%20can%20use%20Python's%20Tkinter,standard%20Windows%20folder%20selection%20dialog.&text=You%20can%20also%20simplify%20this%20and%20write%20tkinter.Tk().

#This offers an explanation on potentially opening the standard Windows file library for file selection. This would be SO CLUTCH in making this more functional in the long-term instead of having to input. Tie it to buttons called "Select..." to pick each individual one for Inv/IFS. Implement by EOD Monday.
