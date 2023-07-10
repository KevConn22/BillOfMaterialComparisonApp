import pandas as pd
from tkinter import *
from tkinter import ttk

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
  return inventor_pn

def create_ifs_list(filename):
  dIFS = pd.read_csv(filename, usecols=['Part Number', 'Part Description', 'Quantity  Per Assembly'])
  ifs_pn = dIFS["Part Number"].values.tolist()
  return ifs_pn

#Function for the process of removing zeroes
def remove_leading_zeros(list_characters):
  while True:
    if list_characters[0] == "0":
      del list_characters[0]
    else:
      break

#Removes leading zeros from inventor_pn list (CSV from IFS does so, so must do so here)
#OBSELETE as of 7/10/23
def update_list_removed_zeros():
  for i in range(len(inv_list)):
    number_list = list(inv_list[i])
    remove_leading_zeros(number_list)
    new_number = ''.join(number_list)
    inv_list[i] = new_number

#Prints output dataframes for Inventor and IFS differences
def print_output1(df1):
  print("In Inventor, not IFS:")
  print("")
  print(df1)

def print_output2(df2):
  print("In IFS, not Inventor:")
  print("")
  print(df2)
  print("")

#Function for overall comparison, taking into account all four functions listed above
#FUNCTION WORKS WHEN PASSED BOTH PARAMETERS AS STRINGS
def compare(*args):
  inv_list = create_inv_list(inv_filename.get() + ".csv")
  ifs_list = create_ifs_list(ifs_filename.get() + ".csv")
  for i in range(len(inv_list)):
    number_list = list(inv_list[i])
    remove_leading_zeros(number_list)
    new_number = ''.join(number_list)
    inv_list[i] = new_number
  common = set(inv_list).intersection(set(ifs_list))
  inv_list = [i for i in inv_list if i not in common]
  ifs_list = [i for i in ifs_list if i not in common]
  inventor_df = pd.DataFrame(inv_list, columns=['Part Number'])
  ifs_df = pd.DataFrame(ifs_list, columns=['Part Number'])
  print_output1(inventor_df)
  print("")
  print_output2(ifs_df)

#TEST CASE: compare("Inventor.csv", "IFS.csv")

#Creates the GUI using Tkinter
root = Tk()
root.title("Inventor v. IFS BOM Comparison")
root.geometry("380x400")

#Sets basic mainframe grid to be used in initial screen
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#Creates the input location for the Inventor filename
inv_filename = StringVar()
inv_filename_entry = ttk.Entry(mainframe, width=12, textvariable=inv_filename)
inv_filename_entry.grid(column=2, row = 2, sticky=(W, E))

#Creates the input location for the IFS filename
ifs_filename = StringVar()
inv_filename_entry = ttk.Entry(mainframe, width=12, textvariable=ifs_filename)
inv_filename_entry.grid(column=2, row=3, sticky=(W, E))

#Creates the submit button (hate this button.)
ttk.Button(mainframe, text="Compare", command=compare).grid(column=2, row=4, sticky=W)

#Creates the labels for IFS and Inventor filename submission boxes
ttk.Label(mainframe, text="Inventor BOM Filename: ").grid(column=1, row=2, sticky=W)
ttk.Label(mainframe, text="IFS BOM Filename: ").grid(column=1, row=3, sticky=E)

#Makes it look more aesthetic by adding padding around each grid element
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=10, pady=10)

root.bind("<Return>", compare)

root.mainloop()
