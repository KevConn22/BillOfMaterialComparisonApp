# Bill of Material CSV Comparison Tool

Intended for work at WestRock Company, this Python application is meant to compare the Inventor Bill of Material (BOM) with the Bill of Material in IFS (MBOM). By automating this process, the goal is to cut down on time taken for BOM comparison, decrease error in the comparison process, decrease engineering workload, and allow for easier engineer/manufacturer communication about BOM differences.

## How To Use

### Without Editing:

If you do not have any edits necessary to the code, then you can download/run the program as follows:

1. Download the .exe that is in Dropbox (https://www.dropbox.com/scl/fi/nfbcl5bv8p3cxtz6qougl/BOM-Comparison.exe?rlkey=44mlgl3l2me15rrm605i0if09&dl=0)
2. Run the program on your local machine. You might be given a message saying it's an unknown program: click "Run Anyway" if this is the case

### With Editing:

If you do have to make edits prior to running the program (or, if you need to edit before redeployment), then the process can be somewhat difficult. You have two options:

#### Option 1:

1. Contact me. I can be reached at 407-451-9980 or at kev.connell.22@gmail.com, and will happily provide ongoing support by modifying, editing, and redeploying this program for future use.

#### Option 2:

##### Step 1: Create a Local IDE
1. Download PyCharm Open Source Edition (Free)
2. Download Python
3. Set interpreter path: in PyCharm, press Ctrl + Alt + S to open IDE settings. Under "Project: ProjectName", click "Python Interpreter". Navigate to your local interpreter, downloaded from Python website.
4. Open a new project in PyCharm. Save as whatever name you would like, it does not matter in the end. Just make sure that the actual file you are writing in is named main.py (you can see the file name on the left hand side, in the project directory)
5. Click on the "File" --> "New Project Setup" --> "Preferences for New Projects". At this point, select your project-specific interpreter from the dropdown menu above: it should say Python [version] and then put your project name at the end. From here, click on the "+" and add in four packages: "pandas", "future", "pyinstaller" and "os.path". To install packages, you search them by name, and then click "Install Package" in the bottom left.
       (For reference, see: https://www.youtube.com/watch?v=i7IjptYwa_g)
7. At this point, your IDE should be set up successfully. Double-check that your interpreter is active (you can see its status in the bottom-right of your main IDE window)

##### Step 2: Accessing/Modifying Source Code
1. Fork this repository to your own GitHub (you can also just copy/paste the code to your local environment, but making your own GitHub repository will allow for version control and cloud sharing)
2. Make edits wherever necessary. More than likely, you will have to edit a category name ("Part Number", "QTY", etc. might have changed in local IFS/Inventor BOM columns)
3. Test using test cases: personally, I used three sets of previously-checked BOMs and ran the program to make sure it worked

##### Step 3: Deployment
1. To deploy to an executable, open a terminal window (you can find the "Terminal" tab at the bottom-center of the main PyCharm IDE window)
2. In the terminal, type the following command: pyinstaller main.py --onefile --windowed
3. If it throws an error, you have to change the authority settings on your device. To do this, open Windows PowerShell (can search using searchbar). In here, type in "set-ExecutionPolicy remotesigned". Then, type in "A" to say Yes to All
4. Go back to PyCharm, and run the following command again: pyinstaller main.py --onefile --windowed
5. Open the folder C:/Users/YourUserName/PyCharm Projects/ProjectName/dist. In this folder, you will find the new executable. Run the executable to make sure it works, and if it does, then it is ready to deploy on other systems

## Design, Packages, Etc.

Languages Used: Python

Packages Used: pandas, tkinter, os.path

## Outcomes

This code, in its current limited usage, has already proven to be extremely beneficial. Manually comparing Bills of Material is something that is tedious and oftentimes results in errors. Based upon a week's worth of work, this was able to reduce error of CSV comparison by 11% and decrease the time taken by ~75% (this number goes even higher as the BOM increases in length). So, it is successful in its current usage, with testing benchmarks to prove it.
