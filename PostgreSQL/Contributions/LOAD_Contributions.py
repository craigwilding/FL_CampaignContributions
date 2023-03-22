import psycopg2
import os
import sys
sys.path.insert(0, '/workspaces/vscode-remote-try-python/PostgreSQL')
import SQLCommands as SQL
import csv
from csv import DictReader


#########################################
# Load the contributions table from the file:
# /DATA/State Races/DBFiles
# /2022HD
# /2022SD
#########################################
table = "contributions"
dirIn = "/workspaces/vscode-remote-try-python/DATA/State Races"
dirIn = os.path.join(dirIn, "DBFiles")
print(dirIn)
dirErrors = os.path.join(dirIn,  "Errors")
fileNameErrors = os.path.join(dirErrors,  "Contrib_LoadErrors.csv")

TAB = "\t"
EOL = '\n'
SINGLE_QT = "'"
SQL_END = ";"

dictErrors = {}
        
def loadCandidates(conn, fileNameIn) :
    
    try :
        cand_id = GetCandidateId(conn, fileNameIn)
        whereSql = " WHERE (cand_id = " + str(cand_id) + ")"
        SQL.DeleteWhere(conn, table, whereSql)
        print("DELETED ROWS for " + table)
        # end with cursor

        SQL.LoadCSV_WithID(conn, table, fileNameIn) 

        SQL.SelectCountWhere(conn, table, whereSql)
        
        # commit data
        conn.commit()

    except Exception as error:
        print ("ERRROR LOADING: " + fileNameIn)
        print(error)
        folders = fileNameIn.split("/")
        fileName = folders[len(folders)-1]
        dictErrors[fileName] = error
        conn.rollback()
    # end try
# loadCandidates

def GetCandidateId(conn, fileNameIn) :
    # Have to get candidate info from the file name
    # as not all candidates have contribution entries to pull the data from


    # get district from filename
    # HD82_REP_Lauren-Uhlich_Melo_contrib_DBFile
    folders = fileNameIn.split("/")
    fileName = folders[len(folders)-1]
    parts = fileName.split('_')
    office = parts[0]
    district = "0"
    if (office.startswith("HD")) :
        district = office[2:]
        office = "STR"
    elif (office.startswith("SD")) :
        district = office[2:]
        office = "STS"
    # end if

    party = parts[1]
    firstName = parts[2]
    lastName = parts[3]
    year = "2022"
        
    # end district


    # start SQL call
    cand_id = ""
    table = "candidates"
    sqlWhere = " WHERE "
    #sqlWhere += " (UPPER(lastname) = '" + lastName.upper() + "')"
    #sqlWhere += " AND (firstname.UPPER() LIKE '%" + firstName.upper() + "%')"
    sqlWhere += " (party = '" + party.upper() + "')"
    sqlWhere += " AND (office = '" + office.upper() + "')"
    sqlWhere += " AND (year = " + year + ")"  # integer
    if ("0" != district) :
        sqlWhere += " AND (district = " + district + ")" # integer
    # endif district

    print(sqlWhere)
    cand_id = SQL.SelectIdWhere(conn, table, sqlWhere)
    # end SQL call


    return cand_id
# end GetCandidateId

######################################################
# CALL LOAD METHOD for HD and SD
#######################################################
# NOTE: Start connection outside of loop so we do not
# go over open connections limit
#########################################
with SQL.Connect() as conn:

    # House District Candidates
    dirDB = os.path.join(dirIn, "2022HD")
    for contribFile in os.listdir(dirDB) :
        print(contribFile)
        fileNameIn = os.path.join(dirDB, contribFile)
        loadCandidates(conn, fileNameIn) 
    # end for 2022HD

    # Senate District Candidates
    dirDB = os.path.join(dirIn, "2022HD")
    for contribFile in os.listdir(dirDB) :
        print(contribFile)
        fileNameIn = os.path.join(dirDB, contribFile)
        loadCandidates(conn, fileNameIn) 
    # end for 2022HD
# end with connection

#########################################################
# WRITE LOAD ERRORS
# Always write load errors.  Leave as empty file if no errors.
#########################################################
if not os.path.exists(dirErrors):
    os.makedirs(dirErrors)
# end if dirErrors
    
with open(fileNameErrors, 'w', newline='') as write_csv:
    # field names 
    fields = ['fileName', 'error']
    # write column headers 
    csvwriter = csv.DictWriter(write_csv, fieldnames = fields)
    csvwriter.writeheader()
    rowsOut = []

    for fileName in dictErrors :
        error = dictErrors[fileName]
        rowOut = {}      
        rowOut["fileName"] = fileName
        rowOut["error"] = error
        rowsOut.append(rowOut)
    # end for county

    csvwriter.writerows(rowsOut)
    print("WRITE file: " + fileNameErrors)
# end with write csv
del write_csv
del rowsOut  