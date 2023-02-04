import os
import shutil
import csv
from csv import DictReader

############################################################
# Fix Bad Data
# Go through the contribution files for state house / senate candidates
# Some have a bad format due to returning bad data as binary
# example: 
# b'Candidate/Committee',b'Date',b'Amount',b'Typ',b'Contributor Name',b'Address',b'City State Zip',b'Occupation',b'Inkind Desc'
############################################################

wrksp = "/workspaces/vscode-remote-try-python/DATA/State Races"
dirHDContrib = os.path.join(wrksp, "2022HD")
print(wrksp)

TAB = "\t"
EOL = '\n'
BAD = '\'"'
FIX = '"'

# Read each file as a csv.  If it cannot read it, then parse to remove errors
for contribFile in os.listdir(dirHDContrib) :
    print(contribFile)
    fileNameIn = os.path.join(dirHDContrib, contribFile)

    try :
        with open(fileNameIn, 'r') as read_obj:
            csv_dict_reader = DictReader(read_obj)
            for row in csv_dict_reader :
                amountStr = row['Amount']
            # end for each row
        # end read csv
        # ignore if no read error
    except :
        # read error
        print("ERROR Reading: " + contribFile)
        linesOut = []
        fileIN = open(fileNameIn, encoding="utf8")
        for line in fileIN :
            lineOut = line.replace("b'","").replace("',",",").replace(BAD,FIX).replace(",'",",").replace(EOL,"")
            linesOut.append(lineOut)
        # end lines
        fileIN.close()
        del fileIN

        fileOut = open(fileNameIn, 'w', encoding='utf8')
        for lineOut in linesOut :
            fileOut.write(lineOut + EOL)
        # end for linesOut
        fileOut.close()
        del fileOut
        del linesOut
    # end except
# end for each file

