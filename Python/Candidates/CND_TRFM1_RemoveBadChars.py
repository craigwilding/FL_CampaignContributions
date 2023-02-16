import os
import shutil
import pandas as pd 

source_encoding = "iso-8859-1"

############################################
# Remove Bad characters that break loading into the database
# Bad characters: " 
############################################
dirIn = "/workspaces/vscode-remote-try-python/DATA/State Races"
dirOut = os.path.join(dirIn,  "DBFiles")
if not os.path.exists(dirOut):
    os.makedirs(dirOut)

TAB = "\t"
EOL = '\n'
COMMA = ','
QUOTE = '"'
SINGLE_QUOTE = "'"
MAX_BYTE_READ = 100000000   # Max file size in Bytes before getting a read failure
textColumns = ['LastName', 'FirstName']
districtColumns = ['District']
textColIndex = [1,2]
#######################################################
# Get each file in the VoterDetail folder
#######################################################

def CanidatesRemoveBadChars(fileNameIn) :
     
    if not os.path.isfile(fileNameIn) :  # Skip DBFiles directory
        return

    print(fileNameIn)
    fileNameOut = fileNameIn.replace(".csv","_DBFile.csv")
    fileNameOut = fileNameOut.replace(dirIn,dirOut)
    print(fileNameOut)
    

    fileSize = os.path.getsize(fileNameIn)
    # print(fileSize)
    if (fileSize < MAX_BYTE_READ) :
        try :  # try with pandas first
            # Read as pandas data frame
            # No header row
            print("Read As Pandas file")
            df = pd.read_csv(fileNameIn,sep=COMMA,header=0,index_col=False, encoding=source_encoding)
            # print("Read file")
            # print(df.head(5))
            # print("Column Types:")
            # print(df.dtypes)

            for colName in textColumns :
                
                # replace non-Asci characters
                df[colName].replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)
                # df[colName].str.encode('ascii', 'ignore').str.decode('ascii')
                #print("encoded column")

                # df[colName].str.replace(QUOTE,SINGLE_QUOTE)
            # end for text columns

            # if district is missing, fill with 0
            for colName in districtColumns :
                df[colName] = df[colName].fillna(0).astype(int)
            # end for district columns
            # print("Fix District columns")
            # print(df.head(5))

            # write back to csv
            df.to_csv(fileNameOut,sep=COMMA, index=False)
            #print("Wrote file")

            # clean up data frames
            del df
        except :
            # pandas failed - could not load large file
            print("Failed with pandas")
        # end try-except
    else :
        # read by line for large files
        fileIn = open(fileNameIn, encoding=source_encoding)
        fileOut = open(fileNameOut, 'w')
        lineCount = 0
        for line in fileIn :

            lineCount = lineCount + 1
            lineOut = ""
            if (1 == lineCount) :
                fileOut.write(line)  # write header
            else :
                columns = line.replace(EOL,"").split(COMMA)
                colIx = -1
                for colVal in columns :
                    colIx += 1
                    value = colVal
                    if (colIx in textColIndex) :
                        # Fix non-utf8 chars
                        columnValDec = value.encode("utf-8")
                        columnValOut = str(columnValDec)
                        value = columnValOut.replace('"',"")

                        # replace quotes
                        #value = value.replace(QUOTE,SINGLE_QUOTE)
                        
                    # end if text column

                    if (colIx > 0) :
                        lineOut += COMMA + value
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
        print("replacing file: " + fileNameOut)
        # shutil.move(fileNameOut, fileNameIn)
    # end if temp exist
# end CanidatesRemoveBadChars

fileNameIn = os.path.join(dirIn, "2022HDCandidates.csv")
CanidatesRemoveBadChars(fileNameIn)

fileNameIn = os.path.join(dirIn, "2022SDCandidates.csv")
CanidatesRemoveBadChars(fileNameIn)