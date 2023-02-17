import psycopg2
import sys
sys.path.insert(0, '/workspaces/vscode-remote-try-python/PostgreSQL')
import SQLCommands as SQL

table = "candidates"
SINGLE_QT = "'"
###########################################
# Create INDEXES on Candidates table
###########################################

with SQL.Connect() as conn:

    ##########################################################
    # Create Indexes
    ##########################################################
    SQL.DropIndex(conn, table, "year")
    SQL.CreateIndex(conn, table, "year")

    SQL.DropIndex(conn, table, "party")
    SQL.CreateIndex(conn, table, "party")

# end with connection - triggers commit
print("****************************")
print("Finished")