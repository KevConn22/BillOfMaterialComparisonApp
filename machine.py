# Library imports necessary for code
import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os.path

"""

What's up!

It's me again, this time trying something that's probably going to be more difficult. Instead of simply running a per-basis comparison, I am instead going to be doing a whole-machine comparison.

Good luck, and let's see the code!

"""

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
