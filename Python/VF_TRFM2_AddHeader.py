import os
import shutil
import pandas as pd 

############################################
# Add column header to DB file
############################################
dirVoterFiles = "/workspaces/vscode-remote-try-python/DATA/VoterFiles"
dirIn = os.path.join(dirVoterFiles,  "DBFiles")
dirOut = dirIn

if not os.path.exists(dirOut):
    os.makedirs(dirOut)

TAB = "\t"
EOL = '\n'
MAX_BYTE_READ = 100000000   # Max file size in Bytes before getting a read failure
columnNames = ['county', 'voterid', 'lastName', 'suffix', 'firstname', 'middle', 'exempt']
columnNames += ['city', 'state', 'zipcode', 'gender', 'race', 'birth_date', 'reg_date']
columnNames += ['party', 'precinct', 'active', 'congress', 'house', 'senate', 'countycom', 'school']
for voterFile in os.listdir(dirIn) :
    
    fileNameIn = os.path.join(dirIn, voterFile)
    outName = voterFile.replace("DBFile", "temp")
    fileNameOut = os.path.join(dirIn, outName)
    if not os.path.isfile(fileNameIn) :  # Skip DBFiles directory
        continue

    # if (voterFile.find("BAY") < 0) :  # Test with BAK
    #   continue
    
    print(voterFile)

    fileSize = os.path.getsize(fileNameIn)
    # print(fileSize)
    if (fileSize < MAX_BYTE_READ) :
        # dataframe
        # Read as pandas data frame
        # No header row
        df = pd.read_csv(fileNameIn,sep=TAB,header=None)
        
        #check if has column headers already
        topline = str(df.head(1))
        if (topline.find('county') < 0) :
            df.columns = columnNames
            df.to_csv(fileNameOut,sep=TAB, index=False)
        else :
            print("header already exists")
        # end if no header

    else :
        fileIn = open(fileNameIn, 'r')
        fileOut = open(fileNameOut, 'w')
        lineCount = 0
        for line in fileIn :
            columns = line.replace(EOL,"").split(TAB)
            if (columns[0] == columnNames[0]) :
                break  # column names already added
            
            lineCount += 1
            if (1 == lineCount) :
                header = ""
                for colName in columnNames :
                    if ("" == header) :
                        header += colName # 1st column
                    else :
                        header += TAB + colName
                    # end if 1st column
                # end for colname header
                fileOut.write(header + EOL)
            # end if header

            fileOut.write(line)
        # end for each line
        fileIn.close()
        del fileIn

        fileOut.close()
        del fileOut
    # end if filesize

    if os.path.exists(fileNameOut):
        print("replacing file: " + fileNameIn)
        shutil.move(fileNameOut, fileNameIn)
    # end if temp exist
# end for directory