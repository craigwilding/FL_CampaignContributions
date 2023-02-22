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



districtColumns = ['District']
# b'Candidate/Committee',b'Date',b'Amount',b'Typ',b'Contributor Name',b'Address',b'City State Zip',b'Occupation',b'Inkind Desc'
dictRenameColumnsBin = {
    "Candidate/Committee'": "candidate",
    "LastName": "lastname",
    "FirstName": "firstname",
    "Party": "party",
    "Status": "status",
    "Primary": "primary_result",
    "General": "general_result"
}

listRemoveColumns = ['MatchType']

def CamapignDonationTransforms(pandasTX) :
    print(pandasTX.fileNameIn)
    pandasTX.removeNonAscii()
    pandasTX.removeBinary()
    pandasTX.removeColumn("Address")
    

# end CamapignDonationTransforms

dirData = "/workspaces/vscode-remote-try-python/DATA/State Races"
dirDBFiles = os.path.join(dirData,  "DBFiles")
if not os.path.exists(dirDBFiles):
    os.makedirs(dirDBFiles)

##############################################
# FL House District Candidates
##############################################
dirIn = os.path.join(dirData, "2022HD")
dirOut = os.path.join(dirDBFiles, "2022HD")
if not os.path.exists(dirOut):
    os.makedirs(dirOut)

for contribFile in os.listdir(dirIn) :
    print(contribFile)
    fileNameIn = os.path.join(dirIn, contribFile)
    outName = contribFile.replace(".csv","_DBFile.csv")
    fileNameOut = os.path.join(dirOut, outName)
    shutil.copy(fileNameIn, fileNameOut)
    pandasTX = PTX.PandasTransform(fileNameOut, delim=COMMA, headers=True)
    CamapignDonationTransforms(pandasTX)
# end for contrib files

##############################################
# FL Senate District Candidates
##############################################
dirIn = os.path.join(dirData, "2022SD")
dirOut = os.path.join(dirDBFiles, "2022SD")
if not os.path.exists(dirOut):
    os.makedirs(dirOut)

for contribFile in os.listdir(dirIn) :
    print(contribFile)
    fileNameIn = os.path.join(dirIn, contribFile)
    outName = contribFile.replace(".csv","_DBFile.csv")
    fileNameOut = os.path.join(dirOut, outName)
    shutil.copy(fileNameIn, fileNameOut)
    pandasTX = PTX.PandasTransform(fileNameOut, delim=COMMA, headers=True)
    CamapignDonationTransforms(pandasTX)
# end for contrib files