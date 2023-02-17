import psycopg2 
import sys
sys.path.insert(0, '/workspaces/vscode-remote-try-python/PostgreSQL')
import SQLCommands as SQL

table = "voters_2022_gen"
listIndexes = ["active", "county", "party", "house", "senate"]

SINGLE_QT = "'"
###########################################
# Create Voter Table
# This holds the voter's data parsed from the voter files
# Street Address information is removed
###########################################

with SQL.Connect()  as conn:

    ##########################################################
    # Create Indexes
    ##########################################################
    for colName in listIndexes :
        try :
            SQL.DropIndex(conn, table, colName)
            SQL.CreateIndex(conn, table, colName)
            conn.commit()
        except Exception as error:
            print("ERRROR creating INDEX: " + table+ "(" + colName + ")")
            print(error)
            conn.rollback()
    # end for each index
# end with connection
print("****************************")
print("Finished")