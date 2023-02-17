import psycopg2
import os
import sys
sys.path.insert(0, '/workspaces/vscode-remote-try-python/PostgreSQL')
import SQLCommands as SQL
import csv
from csv import DictReader

#########################################
# Load the office names from the file:
# offices.csv
#########################################
table = "offices"
dirIn = "/workspaces/vscode-remote-try-python/DATA/State Races"
fileNameIn = os.path.join(dirIn, "Offices.csv")
print(dirIn)

TAB = "\t"
EOL = '\n'
SINGLE_QT = "'"
SQL_END = ";"
        
with SQL.Connect() as conn:
    try :
        SQL.DeleteWhere(conn, table)  # Delete all records

        SQL.LoadCSV(conn, table, fileNameIn) 

        SQL.SelectCountWhere(conn, table)

        conn.commit()

    except Exception as error:
        print ("ERRROR LOADING: " + fileNameIn)
        print(error)
        conn.rollback()
    # end try
# end with connection



