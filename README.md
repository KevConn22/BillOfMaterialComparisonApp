# Bill of Material CSV Comparison Tool

Intended for work at WestRock Company, this Python application is meant to compare the Engineering Bill of Material (EBOM) with the Manufacturing Bill of Material (MBOM). By automating this process, the goal is to cut down on time taken for comparison, error reduction in the comparison process, decreased engineering workload, and enhanced communication between engineering/manufacturing needs and expectations.

## How To Use

### Without Editing:

If you do not have any edits necessary to the code, then you can download/run the program as follows:

1. Download the .exe that is listed in this website ()
2. Run the program on your local machine

### With Editing:

If you do have to make edits prior to running the program (or, if you need to edit before redeployment), then do as follows:

1. Fork this repository to your own GitHub (or simply copy/paste the code where needed)
2. Make edits wherever necessary. More than likely, you will have to edit a category name ("Part Number", "QTY", etc. might have changed in local IFS/Inventor BOM columns)
3. Download/clone repository to local .zip file
4. Package main.py to executable (there are numerous ways in which to do this: my best recommendation would be to Google based upon your specs/situation/IDE if present)
5. Test executable using a 2-3 test cases on your local machine
6. Deploy executable to additional machines

## Design, Packages, Etc.

Languages Used: Python

Packages Used: Pandas, Tkinter



## Outcomes

This code, in its current limited usage, has already proven to be extremely beneficial. Manually comparing Bills of Material is something that is tedious and oftentimes results in errors. Based upon a week's worth of work, this was able to reduce error of CSV comparison by 11% and decrease the time taken by ~33% (this number goes even higher as the BOM increases in length). So, it is successful in its current usage, with testing benchmarks to prove it.
