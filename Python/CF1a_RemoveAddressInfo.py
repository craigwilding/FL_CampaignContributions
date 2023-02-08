import os
import shutil
import pandas as pd 

############################################################
# Remove Address Info
# For security, remove the street address to hide where people live.
# Drop 'Address' column
############################################################

wrksp = "/workspaces/vscode-remote-try-python/DATA/State Races"
print(wrksp)

TAB = "\t"
EOL = '\n'

def removeAddresses(dirIn) :
    addressColumn = 'Address'
    # Read each file as a csv.  If it cannot read it, then parse to remove errors
    for contribFile in os.listdir(dirIn) :
        print(contribFile)
        fileNameIn = os.path.join(dirIn, contribFile)

        # load into pandas data
        dataFrame = pd.read_csv(fileNameIn)
        listColumnNames = list(dataFrame.columns)
        if (addressColumn in listColumnNames) :
            # Drop 'Address' column
            dataFrame.pop(addressColumn)
            # write back to csv
            dataFrame.to_csv(fileNameIn)
        # end if Address Column exists

    # end for each file
# end removeAddresses

dirHDContrib = os.path.join(wrksp, "2022HD")
removeAddresses(dirHDContrib)

dirSDContrib = os.path.join(wrksp, "2022SD")
removeAddresses(dirSDContrib)