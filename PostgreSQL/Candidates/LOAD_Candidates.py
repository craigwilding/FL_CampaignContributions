import psycopg2
import os
import csv
from csv import DictReader

#########################################
# Load the candidates table names from the file:
# 2022HDCandidates.csv
# 2022DDCandidates.csv
#########################################
dirIn = "/workspaces/vscode-remote-try-python/DATA/State Races"
dirIn = os.path.join(dirIn, "DBFiles")
print(dirIn)

TAB = "\t"
EOL = '\n'
SINGLE_QT = "'"
SQL_END = ";"
        
def loadCandidates(fileNameIn, year, office) :
    with psycopg2.connect( host='localhost', user='postgres', password='postgres', dbname='postgres') as conn:
        try :
            with conn.cursor() as cur:
                # delete any previous records
                sql = "DELETE FROM candidates"
                sql += " WHERE (year = " + str(int(year)) + ") AND (office = " + SINGLE_QT + office + SINGLE_QT + ")"
                print(sql)
                cur.execute(sql)
                print("DELETED ROWS for " + "candidates")
            # end with cursor

            with conn.cursor() as cur:    
                # load from DB File
                fileSize = os.path.getsize(fileNameIn)
                print("Loading table: " + "candidates" + " filesize: " + str(fileSize))
                with open(fileNameIn, 'r') as dbFile:
                    #dbFile , <tabe name>, tab-Seperated
                    table = 'candidates'
                    columns = getColumnNames(table)
                    columns.remove("id")
                    print(columns)
                    columnNames = ','.join(columns)
                    sql = f"copy {table}({columnNames}) " # from stdout (format csv header)"
                    sql += " FROM  STDIN " # have to read file into STDIN
                    sql += " DELIMITER E',' CSV HEADER"  # COMMA delimited with header
                    sql += SQL_END
                    print(sql)
                    cur.copy_expert(sql, dbFile, fileSize)
                # end with dbFile
            # end with cursor

            with conn.cursor() as cur:
                # select count
                sql = "SELECT COUNT(*) FROM candidates"
                sql += " WHERE (year = " + str(int(year)) + ") AND (office = " + SINGLE_QT + office + SINGLE_QT + ")"
                print(sql)
                cur.execute(sql)
                recordCount = cur.fetchone()
                print("LOADED " + str(recordCount) + " ROWS for " + "candidates")
            # end with cursor
            
            # commit data
            conn.commit()

        except Exception as error:
            print ("ERRROR LOADING: " + fileNameIn)
            print(error)
            conn.rollback()
        # end try
    # end with connection
# loadCandidates

#####################################################
# Get Column Names from a table
# This is used when loading a table with a serial ID
# to return the non-ID columns being loaded
#####################################################
def getColumnNames(tableName) :
    columnNames = []
    with psycopg2.connect( host='localhost', user='postgres', password='postgres', dbname='postgres') as conn:
        with conn.cursor() as cur:
            # Select column names for table
            sql = "SELECT column_name from information_schema.columns where table_schema = 'public' and table_name='" + tableName + "'"
            cur.execute(sql)
            columnNames = [row[0] for row in cur]

            # print("Column names: {}\n".format(columnNames))
            # end with cursor
    # end connection
    print("Column names: " + str(columnNames))
    return columnNames
# end getColumnNames

getColumnNames('candidates')

# House District Candidates
fileName = "2022HDCandidates_DBFile.csv"
fileNameIn = os.path.join(dirIn, fileName)
loadCandidates(fileNameIn, "2022", "STR") 

# Senate District Candidates
fileName = "2022SDCandidates_DBFile.csv"
fileNameIn = os.path.join(dirIn, fileName)
loadCandidates(fileNameIn, "2022", "STS") 