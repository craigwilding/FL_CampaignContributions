import os
import shutil
import pandas as pd 

############################################
# Add year and office column to Candidates data
# In: 2022HDCandidates.csv, 2022SDCandidates.csv
# Out: 2022HDCandidates_DBFile.csv
# The input files have all the fields for the candidates table
# except the id, year, and office which is in the file name.
# This adds the year and office column to the beginning so we have a DB file available for LOAD_Candidates.py
# The id fields is not added because it is a serial auto-increment.
############################################
dirIn = "/workspaces/vscode-remote-try-python/DATA/State Races"
dirOut = os.path.join(dirIn,  "DBFiles")

TAB = "\t"
COMMA = ','
EOL = '\n'
MAX_BYTE_READ = 100000000   # Max file size in Bytes before getting a read failure

# Dictionary of columns to rename
# key = old Name : value = new Name
# if new name is empty, then remove the column
dictRenameColumns = {
    "District": "district",
    "LastName": "lastname",
    "FirstName": "firstname",
    "Party": "party",
    "Status": "status",
    "Primary": "primary_result",
    "General": "general_result"
}
print(dictRenameColumns)
listRemoveColumns = ['MatchType']

def RenameColumns(fileNameIn) :
    
    fileNameOut = fileNameIn.replace("_DBFile", "_temp3")  # Include _ to avoid directory path
    if not os.path.exists(dirOut):
        os.makedirs(dirOut)
    if not os.path.isfile(fileNameIn) :  # Skip DBFiles directory
        return
    print(fileNameIn)
    print(fileNameOut)

    fileSize = os.path.getsize(fileNameIn)
    # print(fileSize)
    if (fileSize < MAX_BYTE_READ) :
        # dataframe
        # Read as pandas data frame
        df = pd.read_csv(fileNameIn,sep=COMMA,header=0,index_col=False)

        # rename columns
        df.rename(columns=dictRenameColumns, inplace=True)

        listColumnNames = list(df.columns)
        for colName in listRemoveColumns :
            if (colName in listColumnNames) :
                df.pop(colName)
            #else :
                # column does not exist
            # end if
        # end for remove columns

        df.to_csv(fileNameOut,sep=COMMA, index=False)
        

    else :
        print("ERROR: file to large for pandas: " + str(fileSize))

    # end if filesize

    if os.path.exists(fileNameOut):
        # copy temp to original
        print("Replacing DB file: " + fileNameIn)
        shutil.move(fileNameOut, fileNameIn)
    # end if
# end AddYearAndOffice

dirOut = os.path.join(dirIn,  "DBFiles")

# House District Candidates
fileName = "2022HDCandidates_DBFile.csv"
fileNameIn = os.path.join(dirOut, fileName)
RenameColumns(fileNameIn) 

# Senate District Candidates
fileName = "2022SDCandidates_DBFile.csv"
fileNameIn = os.path.join(dirOut, fileName)
RenameColumns(fileNameIn) 