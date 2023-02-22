import os
import shutil
import pandas as pd 
import PandasTransforms as PTX

############################################
# TRANSFORM Candidate data
# Perform any data transformations here before loading to database
# fileNameIn =  2022HDCandidates.csv - Florida State House District Candidates
#               2022SDCandidates.csv  - Florida State Senate District Candidates
# dirOut = DBFiles   
#    This creates a copy of the original into the DBFiles subfolder with a _DBFile.csv extension
############################################

TAB = "\t"
EOL = '\n'
COMMA = ','

dirIn = "/workspaces/vscode-remote-try-python/DATA/State Races"
dirOut = os.path.join(dirIn,  "DBFiles")
if not os.path.exists(dirOut):
    os.makedirs(dirOut)

districtColumns = ['District']
dictRenameColumns = {
    "District": "district",
    "LastName": "lastname",
    "FirstName": "firstname",
    "Party": "party",
    "Status": "status",
    "Primary": "primary_result",
    "General": "general_result"
}

listRemoveColumns = ['MatchType']

def CandidateTransforms(pandasTX, year, office) :
    print(pandasTX.fileNameIn)
    pandasTX.removeNonAscii()
    pandasTX.addColumn('office', office, colLocation=PTX.COL_BEGIN)
    pandasTX.addColumn('year', year, colLocation=PTX.COL_BEGIN)
    pandasTX.setNullValues(districtColumns, "0")
    pandasTX.renameColumn(dictRenameColumns)
    for colName in listRemoveColumns :
        pandasTX.removeColumn(colName)
    # end for listRemoveColumns

# end CandidateTransforms

##############################################
# FL House District Candidates
##############################################
fileNameIn = os.path.join(dirIn, "2022HDCandidates.csv")
fileNameOut = fileNameIn.replace(".csv","_DBFile.csv")
fileNameOut = fileNameOut.replace(dirIn,dirOut)
shutil.copy(fileNameIn, fileNameOut)
pandasTX = PTX.PandasTransform(fileNameOut, delim=COMMA, headers=True)
CandidateTransforms(pandasTX, "2022", 'STR')

##############################################
# FL Senate District Candidates
##############################################
fileNameIn = os.path.join(dirIn, "2022SDCandidates.csv")
fileNameOut = fileNameIn.replace(".csv","_DBFile.csv")
fileNameOut = fileNameOut.replace(dirIn,dirOut)
shutil.copy(fileNameIn, fileNameOut)
pandasTX = PTX.PandasTransform(fileNameOut, delim=COMMA, headers=True)
CandidateTransforms(pandasTX, "2022", 'STS')