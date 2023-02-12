import os
import shutil
import pandas as pd 

############################################
# Remove Exempt records from voter file
# exempt records causes load errors
############################################
dirVoterFiles = "/workspaces/vscode-remote-try-python/DATA/VoterFiles"
dirDBFiles = os.path.join(dirVoterFiles,  "DBFiles")
dirOut = dirDBFiles
if not os.path.exists(dirOut):
    os.makedirs(dirOut)

TAB = "\t"
EOL = '\n'
MAX_BYTE_READ = 100000000   # Max file size in Bytes before getting a read failure
columnNames = ['county', 'voterid', 'lastName', 'suffix', 'firstname', 'middle', 'exempt']
columnNames += ['city', 'state', 'zipcode', 'gender', 'race', 'birth_date', 'reg_date']
columnNames += ['party', 'precinct', 'active', 'congress', 'house', 'senate', 'countycom', 'school']
#######################################################
# Get each file in the VoterDetail folder
#######################################################

for voterFile in os.listdir(dirDBFiles) :
    
    fileNameIn = os.path.join(dirDBFiles, voterFile)
    if not os.path.isfile(fileNameIn) :  # Skip DBFiles directory
        continue

    #if (voterFile.find("DAD") < 0) :  # Test with BAK
    #    continue

    print(voterFile)
    county = voterFile[0:3]
    fileNameOut = os.path.join(dirOut, county + "_temp3.txt")

    fileSize = os.path.getsize(fileNameIn)
    # print(fileSize)
    if (fileSize < MAX_BYTE_READ) :
        try :  # try with pandas first
            # Read as pandas data frame
            # No header row
            df = pd.read_csv(fileNameIn,sep=TAB,header=0,index_col=False)
            # print("Read file")
            # print(df.head(10))

            
            dfNoExempt = df[df.exempt != 'Y']
            print("Removed exempt")
            print(dfNoExempt.head(10))

            # write back to csv
            
            dfNoExempt.to_csv(fileNameOut,sep=TAB, index=False)
            #print("Wrote file")

            # clean up data frames
            del df
            del dfNoExempt
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
                exempt = columns[6]
                if ('N' == exempt) :
                    fileOut.write(line)  # write row
                # end if exempt
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
