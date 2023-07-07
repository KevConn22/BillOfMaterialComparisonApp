import pandas as pd
"""
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

#Creates the dataframe for each particular document, both the Inventor and IFS CSVs.
dIFS = pd.read_csv(
  "IFS.csv",
  usecols=['Part Number', 'Part Description', 'Quantity  Per Assembly'])
dI = pd.read_csv("Inventor.csv", usecols=['Part Number', 'Description', 'QTY'])

#Takes the part number columns and creates lists of each p/n column
inventor_pn = dI["Part Number"].values.tolist()
ifs_pn = dIFS["Part Number"].values.tolist()

#Function for the process of removing zeroes
def remove_leading_zeros(list_characters):
  while True:
    if list_characters[0] == "0":
      del list_characters[0]
    else:
      break

#Removes leading zeros from inventor_pn list (CSV from IFS does so, so must do so here)
def update_list_removed_zeros():
  for i in range(len(inventor_pn)):
    number_list = list(inventor_pn[i])
    remove_leading_zeros(number_list)
    new_number = ''.join(number_list)
    inventor_pn[i] = new_number

update_list_removed_zeros()

#print(inventor_pn)
#print("")
#print(ifs_pn)
#print("")

#Finds common values, then prints the differences within each list by deleting common values from each list
common = set(inventor_pn).intersection(set(ifs_pn))
inventor_pn = [i for i in inventor_pn if i not in common]
ifs_pn = [i for i in ifs_pn if i not in common]

inventor_df = pd.DataFrame(inventor_pn, columns=['Part Number'])
ifs_df = pd.DataFrame(ifs_pn, columns=['Part Number'])

print("In Inventor, not IFS:")
print("")
print(inventor_df)
print("")
print("In IFS, not Inventor:")
print("")
print(ifs_df)
print("")

#Creates list of common of part numbers between both, including the negated leading zeros
list_common = list(common)


"""
data_final = {
  'Inventor P/N': [],
  'in IFS? (T/F)': [],
  'IFS P/N': [],
  'in Inventor?': [],
  
  
}
"""
