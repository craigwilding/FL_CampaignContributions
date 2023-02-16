import psycopg2
import os
import csv
from csv import DictReader

#########################################
# Load the office names from the file:
# offices.csv
#########################################
dirIn = "/workspaces/vscode-remote-try-python/DATA/State Races"
fileNameIn = os.path.join(dirIn, "Offices.csv")
print(dirIn)

TAB = "\t"
EOL = '\n'
SINGLE_QT = "'"
SQL_END = ";"
        
with psycopg2.connect( host='localhost', user='postgres', password='postgres', dbname='postgres') as conn:
    try :
        with conn.cursor() as cur:
            # delete any previous records
            sql = "DELETE FROM offices"
            print(sql)
            cur.execute(sql)
            print("DELETED ROWS for " + "offices")
            
            # load voters from DB File
            sql = "COPY offices"
            sql += " FROM  STDIN " # have to read file into STDIN
            sql += " DELIMITER E',' CSV HEADER;"  # TAB delimited with header
            sql += SQL_END
            fileSize = os.path.getsize(fileNameIn)
            print("Loading table: " + "offices.csv" + " filesize: " + str(fileSize))
            with open(fileNameIn, 'r') as dbFile:
                #dbFile , <tabe name>, tab-Seperated
                # cur.copy_from(dbFile, "voters_2022_gen", sep='\t') # doesn't allow headers
                cur.copy_expert(sql, dbFile, fileSize)
            # end with dbFile

            # select count
            sql = "SELECT COUNT(code) FROM offices"
            print(sql)
            cur.execute(sql)
            recordCount = cur.fetchone()
            print("LOADED " + str(recordCount) + " ROWS for " + "offices")

            # commit data
            conn.commit()
        # end with cursor

    except Exception as error:
        print ("ERRROR LOADING: " + fileNameIn)
        print(error)
        conn.rollback()
    # end try
# end with connection



