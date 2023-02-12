import os
import shutil
import pandas as pd 

############################################
# Read original voter files from FL DOE
# transform into the columns we want
# remove address columns
############################################
dirVoterFiles = "/workspaces/vscode-remote-try-python/DATA/VoterFiles"
dirOut = os.path.join(dirVoterFiles,  "DBFiles")
if not os.path.exists(dirOut):
    os.makedirs(dirOut)

TAB = "\t"
EOL = '\n'
MAX_BYTE_READ = 100000000   # Max file size in Bytes before getting a read failure
#######################################################
# Get each file in the VoterDetail folder
#######################################################
removeColumns = [7, 8, 12, 13,14,15,16,17,18, 25,26,27, 34,35,36,37]
for voterFile in os.listdir(dirVoterFiles) :
    
    fileNameIn = os.path.join(dirVoterFiles, voterFile)
    if not os.path.isfile(fileNameIn) :  # Skip DBFiles directory
        continue

    if (voterFile.find("BAY") < 0) :  # Test with BAK
        continue

    print(voterFile)
    county = voterFile[0:3]
    fileNameOut = os.path.join(dirOut, county + "_DBFile.txt")

    fileSize = os.path.getsize(fileNameIn)
    # print(fileSize)
    if (fileSize < MAX_BYTE_READ) :
        try :  # try with pandas first
            # Read as pandas data frame
            # No header row
            df = pd.read_csv(fileNameIn,sep=TAB,header=None)
            #print("Read file")
            #print(df.head(5))

            # Remove address columns: 7, 8, 12-18
            # unused precinct data: 25-27
            # Remove phone and email columns: 34 - 37
            
            colCount = len(df.axes[1])
            dfNoAddr = df.drop(df.columns[removeColumns],axis = 1)
            #print("Removed columns")
            #print(dfNoAddr.head(5))

            # write back to csv
            
            dfNoAddr.to_csv(fileNameOut,sep=TAB, header=False, index=False)
            # print("Wrote file")

            # clean up data frames
            del df
            del dfNoAddr
        except :
            # pandas failed - could not load large file
            print("Failed with pandas")
        # end try-except
    else :
        # read by line for large files
        fileIn = open(fileNameIn, 'r')
        fileOut = open(fileNameOut, 'w')
        lineCount = 0
        for line in fileIn :

            lineCount = lineCount + 1
            # skip column names


            columns = line.replace(EOL,"").split(TAB)
            colCount = 0
            lineOut = ""
            for col in columns :
                if (colCount not in removeColumns) :
                    # copy column value to lineOut
                    if (colCount > 0) :
                        lineOut += TAB + col
                    else :
                        lineOut += col
                    # end if colCount
                # end if not in removeColumns
                colCount += 1
            # end for columns
            fileOut.write(lineOut + EOL)
        # end for line
        fileIn.close()
        fileOut.close()
        del fileIn
        del fileOut
    # end if file size

# end for each voter file
print("*******************************")
print("*******************************")
print("Finished")