import os
import shutil
import pandas as pd 

############################################
# Add year and office column to Candidates data
# In: 2022HDCandidates.csv, 2022SDCandidates.csv
# Out: 2022HDCandidates_DBFile.csv
# The input files have all the fields for the candidates table
# except the id, year, and office which is in the file name.
# This adds the year and office column to the beginning so we have a DB file available for LOAD_Candidates.py
# The id fields is not added because it is a serial auto-increment.
############################################
dirIn = "/workspaces/vscode-remote-try-python/DATA/State Races"
dirOut = os.path.join(dirIn,  "DBFiles")

TAB = "\t"
COMMA = ','
EOL = '\n'
MAX_BYTE_READ = 100000000   # Max file size in Bytes before getting a read failure

def AddYearAndOffice(fileNameIn, yearVal, officeVal) :
    
    fileNameOut = fileNameIn.replace("_DBFile", "_temp2")  # Include _ to avoid directory path
    if not os.path.exists(dirOut):
        os.makedirs(dirOut)
    if not os.path.isfile(fileNameIn) :  # Skip DBFiles directory
        return
    print(fileNameIn)
    print(fileNameOut)

    fileSize = os.path.getsize(fileNameIn)
    # print(fileSize)
    if (fileSize < MAX_BYTE_READ) :
        # dataframe
        # Read as pandas data frame
        df = pd.read_csv(fileNameIn,sep=COMMA,header=0,index_col=False)
        
        #check if has column headers already
        topline = str(df.head(1))
        if (topline.find('office') < 0) :
            df.insert(0,'office','')
            df['office'] = officeVal
        else :
            print("office column already exists")
        # end if office

        if (topline.find('year') < 0) :
            df.insert(0,'year','')
            df['year'] = yearVal
        else :
            print("year column already exists")
        # end if office

        df.to_csv(fileNameOut,sep=COMMA, index=False)

    else :
        fileIn = open(fileNameIn, 'r')
        fileOut = open(fileNameOut, 'w')
        lineCount = 0
        for line in fileIn :
            columns = line.replace(EOL,"").split(TAB)
            if (columns[0] == 'year') :
                break  # column names already added
            
            lineCount += 1
            if (1 == lineCount) :
                header = "year,office," + line
                fileOut.write(header)
            else :
                lineOut = str(yearVal) + COMMA + str(officeVal) + COMMA + line
                fileOut.write(lineOut)
            # end if header

            fileOut.write(line)
        # end for each line
        fileIn.close()
        del fileIn

        fileOut.close()
        del fileOut
    # end if filesize

    if os.path.exists(fileNameOut):
        # copy temp to original
        print("Replacing DB file: " + fileNameIn)
        shutil.move(fileNameOut, fileNameIn)
    # end if
# end AddYearAndOffice

dirOut = os.path.join(dirIn,  "DBFiles")

# House District Candidates
fileName = "2022HDCandidates_DBFile.csv"
fileNameIn = os.path.join(dirOut, fileName)
AddYearAndOffice(fileNameIn, "2022", "STR") 

# Senate District Candidates
fileName = "2022SDCandidates_DBFile.csv"
fileNameIn = os.path.join(dirOut, fileName)
AddYearAndOffice(fileNameIn, "2022", "STS") 