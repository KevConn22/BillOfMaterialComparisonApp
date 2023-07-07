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

dI = pd.read_csv(
  "Test1.csv",
  usecols=['Part Number', 'Part Description', 'Quantity  Per Assembly'])
dIFS = pd.read_csv("Test2.csv", usecols=['Part Number', 'Description', 'QTY'])
print(dI)
print("")
print(dIFS)


"""
Potential final directory for additions?
data_final = {
  'Inventor P/N': [],
  'in IFS? (T/F)': [],
  'IFS P/N': [],
  'in Inventor?': [],
  
  
}
"""
