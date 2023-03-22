import psycopg2
import os
import sys
sys.path.insert(0, '/workspaces/vscode-remote-try-python/PostgreSQL')
import SQLCommands as SQL
import csv
from csv import DictReader


#########################################
# Load the candidates table names from the file:
# 2022HDCandidates.csv
# 2022DDCandidates.csv
#########################################
table = "candidates"
dirIn = "/workspaces/vscode-remote-try-python/DATA/State Races"
dirIn = os.path.join(dirIn, "DBFiles")
print(dirIn)

TAB = "\t"
EOL = '\n'
SINGLE_QT = "'"
SQL_END = ";"

listErrors = []
        
def loadCandidates(fileNameIn, year, office) :
    with SQL.Connect() as conn:
        try :
            whereSql = " WHERE (year = " + str(int(year)) + ") AND (office = " + SINGLE_QT + office + SINGLE_QT + ")"
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
            listErrors.append(error)
            conn.rollback()
        # end try
    # end with connection
# loadCandidates


# House District Candidates
fileName = "2022HDCandidates_DBFile.csv"
fileNameIn = os.path.join(dirIn, fileName)
loadCandidates(fileNameIn, "2022", "STR") 

# Senate District Candidates
fileName = "2022SDCandidates_DBFile.csv"
fileNameIn = os.path.join(dirIn, fileName)
loadCandidates(fileNameIn, "2022", "STS") 

print(listErrors)