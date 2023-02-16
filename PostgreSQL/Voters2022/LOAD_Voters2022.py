import psycopg2
import os
import csv
from csv import DictWriter

###########################################
# Load Voter Table
# This loads the DBFiles from the transform operation
###########################################
dirVoterFiles = "/workspaces/vscode-remote-try-python/DATA/VoterFiles"
dirIn = os.path.join(dirVoterFiles,  "DBFiles")
dirErrors = os.path.join(dirVoterFiles,  "Errors")
fileNameErrors = os.path.join(dirErrors,  "VF_LoadErrors.csv")

TAB = "\t"
EOL = '\n'
SINGLE_QT = "'"
SQL_END = ";"

dictErrors = {}

for voterFile in os.listdir(dirIn) :
    with psycopg2.connect( host='localhost', user='postgres', password='postgres', dbname='postgres') as conn:

        fileNameIn = os.path.join(dirIn, voterFile)
        if not os.path.isfile(fileNameIn) :  # Skip DBFiles directory
            continue

        #if (voterFile.find("PAL") < 0) :  # Test with BAK
        #    continue

        print(voterFile)
        county = voterFile[0:3]

        try :
            with conn.cursor() as cur:
                # delete any previous records for the county
                sql = "DELETE FROM voters_2022_gen WHERE county = " + SINGLE_QT + county + SINGLE_QT + SQL_END
                print(sql)
                cur.execute(sql)
                print("DELETED ROWS for " + county)
            
                # load voters from DB File
                sql = "COPY voters_2022_gen"
                sql += " FROM  STDIN " # have to read file into STDIN
                sql += " DELIMITER E'\t' CSV HEADER;"  # TAB delimited with header
                sql += SQL_END
                fileSize = os.path.getsize(fileNameIn)
                print("Loading table: " + county + " filesize: " + str(fileSize))
                with open(fileNameIn, 'r') as dbFile:
                    #dbFile , <tabe name>, tab-Seperated
                    # cur.copy_from(dbFile, "voters_2022_gen", sep='\t') # doesn't allow headers
                    cur.copy_expert(sql, dbFile, fileSize)
                # end with dbFile

                # select count
                sql = "SELECT COUNT(voterid) FROM voters_2022_gen"
                sql += " WHERE county = " + SINGLE_QT + county + SINGLE_QT + SQL_END
                print(sql)
                cur.execute(sql)
                recordCount = cur.fetchone()
                print("LOADED " + str(recordCount) + " ROWS for " + county)

                # commit data
                conn.commit()
            # end with cursor

            # delete DBFile
            os.remove(fileNameIn)
        except Exception as error:
            print ("ERRROR LOADING: " + county)
            print(error)
            dictErrors[county] = error
            conn.rollback()
        # end try
    # end with connection
# end for db files

#########################################################
# WRITE LOAD ERRORS
# Always write load errors.  Leave as empty file if no errors.
#########################################################
if not os.path.exists(dirErrors):
    os.makedirs(dirErrors)
# end if dirErrors
    
with open(fileNameErrors, 'w', newline='') as write_csv:
    # field names 
    fields = ['county', 'error']
    # write column headers 
    csvwriter = csv.DictWriter(write_csv, fieldnames = fields)
    csvwriter.writeheader()
    rowsOut = []

    for county in dictErrors :
        error = dictErrors[county]
        rowOut = {}      
        rowOut["county"] = county
        rowOut["error"] = error
        rowsOut.append(rowOut)
    # end for county

    csvwriter.writerows(rowsOut)
    print("WRITE file: " + fileNameErrors)
# end with write csv
del write_csv
del rowsOut  

 
print(dictErrors)
del dictErrors


print("****************************")
print("Finished")