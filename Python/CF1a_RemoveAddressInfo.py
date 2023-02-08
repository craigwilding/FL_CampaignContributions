import os
import shutil
import pandas as pd 

############################################################
# Remove Address Info
# For security, remove the street address to hide where people live.
# Drop 'Address' column
############################################################

wrksp = "/workspaces/vscode-remote-try-python/DATA/State Races"
dirHDContrib = os.path.join(wrksp, "2022HD")
print(wrksp)

TAB = "\t"
EOL = '\n'

# Read each file as a csv.  If it cannot read it, then parse to remove errors
for contribFile in os.listdir(dirHDContrib) :
    print(contribFile)
    fileNameIn = os.path.join(dirHDContrib, contribFile)

    # load into pandas data
    dataFrame = pd.read_csv(fileNameIn)
    # Drop 'Address' column
    dataFrame.pop('Address')
    # write back to csv
    dataFrame.to_csv(fileNameIn)

# end for each file