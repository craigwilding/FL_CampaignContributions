import os
import shutil
import pandas as pd 

############################################
# Remove Bad characters that break loading into the database
# Bad characters: " 
############################################
dirVoterFiles = "/workspaces/vscode-remote-try-python/DATA/VoterFiles"
dirDBFiles = os.path.join(dirVoterFiles,  "DBFiles")
dirOut = dirDBFiles
if not os.path.exists(dirOut):
    os.makedirs(dirOut)

TAB = "\t"
EOL = '\n'
QUOTE = '"'
SINGLE_QUOTE = "'"
MAX_BYTE_READ = 100000000   # Max file size in Bytes before getting a read failure
textColumns = ['lastName', 'suffix', 'firstname', 'middle','city' ]
districtColumns = ['congress', 'house', 'senate', 'countycom', 'school']
textColIndex = [2,3,4,5,7]
#######################################################
# Get each file in the VoterDetail folder
#######################################################

for voterFile in os.listdir(dirDBFiles) :
    
    fileNameIn = os.path.join(dirDBFiles, voterFile)
    if not os.path.isfile(fileNameIn) :  # Skip DBFiles directory
        continue

    #if (voterFile.find("ORA") < 0) :  # Test with BAK
    #    continue

    print(voterFile)
    county = voterFile[0:3]
    fileNameOut = os.path.join(dirOut, county + "_temp4.txt")

    fileSize = os.path.getsize(fileNameIn)
    # print(fileSize)
    if (fileSize < MAX_BYTE_READ) :
        try :  # try with pandas first
            # Read as pandas data frame
            # No header row
            df = pd.read_csv(fileNameIn,sep=TAB,header=0,index_col=False)
            print("Read file")
            print(df.head(5))
            # print("Column Types:")
            # print(df.dtypes)

            for colName in textColumns :
                df[colName].str.replace(QUOTE,SINGLE_QUOTE)
            # end for text columns
            # print("Fix Text columns")
            # print(df.head(5))

            # If precinct is blank, replace with 0
            df['precinct'] = df['precinct'].fillna('0')

            # if district is missing, fill with 0
            for colName in districtColumns :
                df[colName] = df[colName].fillna(0).astype(int)
            # end for district columns
            # print("Fix District columns")
            # print(df.head(5))

            # write back to csv
            df.to_csv(fileNameOut,sep=TAB, index=False)
            #print("Wrote file")

            # clean up data frames
            del df
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
            lineOut = ""
            if (1 == lineCount) :
                fileOut.write(line)  # write header
            else :
                columns = line.replace(EOL,"").split(TAB)
                colIx = -1
                for colVal in columns :
                    colIx += 1
                    value = colVal
                    if (colIx in textColIndex) :
                        value = value.replace(QUOTE,SINGLE_QUOTE)
                    # end if text column

                    if (colIx > 0) :
                        lineOut += TAB + value
                    else :
                        lineOut += value
                    # end if first column
                # end for columns
                fileOut.write(lineOut + EOL)
            # end if lineCount
        # end for line
            
        fileIn.close()
        fileOut.close()
        del fileIn
        del fileOut
    # end if file size

    if os.path.exists(fileNameOut):
        print("replacing file: " + fileNameIn)
        shutil.move(fileNameOut, fileNameIn)
    # end if temp exist
# end for each voter file
