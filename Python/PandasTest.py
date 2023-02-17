import os
import shutil
import pandas
import PandasTransforms as PTX

TAB = "\t"
EOL = '\n'
COMMA = ','

######################################################
###### TEST PandasTransform methods
######################################################
dirIn = "/workspaces/vscode-remote-try-python/DATA/TEST"
dirOut = os.path.join(dirIn,  "DBFiles")
if not os.path.exists(dirOut):
    os.makedirs(dirOut)


def GetFirstColumn(fileNameIn, delim=COMMA) :
    # this is used to test the results
    fileIn = open(fileNameIn, encoding='utf-8')
    lineCount = 0
    firstColumn = ""
    for line in fileIn :
        columns = line.split(delim)
        firstColumn = columns[0]
        break
    # end for each line
    fileIn.close()
    del fileIn

    return firstColumn
# end GetFirstColumn

def GetRowColumn(fileNameIn, rowNum, colNum, delim=COMMA) :
    # this is used to test the results
    testVal = ""
    fileIn = open(fileNameIn, encoding='utf-8')
    rowCount = 0
    for line in fileIn :
        rowCount += 1
        if (rowNum != rowCount) :
            continue

        columns = line.replace(EOL,"").split(delim)
        colCount = 0
        for col in columns :
            colCount += 1
            if (colNum == colCount) :
                testVal = col
            # end if
        # end for columns
    # end for each line
    fileIn.close()
    del fileIn

    return testVal
# end GetRowColumn

def PrintRowColumns(fileNameIn, delim=COMMA) :
    # this is used to print the testresults
    fileIn = open(fileNameIn, encoding='utf-8')
    rowCount = 0
    for line in fileIn :
        rowCount += 1

        columns = line.replace(EOL,"").split(delim)
        colCount = 0
        for col in columns :
            colCount += 1
            print("Row: " + str(rowCount) + " Col: " + str(colCount) + " value: " + str(col))
        # end for columns
    # end for each line
    fileIn.close()
    del fileIn

# end GetRowColumn

def TabFileTest(fileNameIn, delim=COMMA,headersIn=True) :
    fileNameOut = fileNameIn.replace(".", "_tabtest.")

    headerVal=0
    if (headersIn != True) :
        headerVal = None
    # end headerVal
    # Read as pandas data frame
    df = pandas.read_csv(fileNameIn,sep=delim,header=headerVal,index_col=False)
    # write to temp file
    df.to_csv(fileNameOut, encoding='utf-8', index=False, header=headersIn, sep=delim)
    # replace in File with temp file
    shutil.move(fileNameOut, fileNameIn)
# end TabFileTest

#################################################
# CSV file, has non-ascii characters, No header
#################################################
fileNameIn = os.path.join(dirIn,  "TestBadChars.csv")
# copy to DBFile
fileNameOut = os.path.join(dirOut,  "TestBadChars_DBFile.csv")
shutil.copy(fileNameIn, fileNameOut)
PTX.removeNonAscii(fileNameOut, PTX.COMMA, False)
test = GetRowColumn(fileNameOut, 1, 1)
if ("Dj vu" == test) :
    print("Remove Ascii from CSV NO HEADER " + "SUCCESS")
else :
    print("Remove Ascii from CSV NO HEADER " + "FAIL")
    PrintRowColumns(fileNameOut, delim=COMMA)
# end test
PTX.addColumn(fileNameOut, "", "End1", headersIn=False)
test = GetRowColumn(fileNameOut, 1, 3)
if ("End1" == test) :
    print("Add Column to END, CSV NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Add Column to END, CSV NO HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=COMMA)
# end test
PTX.addColumn(fileNameOut, "Colstart1", "start1", headersIn=False, colLocation=PTX.COL_BEGIN)
test = GetRowColumn(fileNameOut, 1, 1)
if ("start1" == test) :
    print("Add Column to START, CSV NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Add Column to START, CSV NO HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=COMMA) 
# end test
PTX.removeColumn(fileNameOut, "3", headers=False)
test = GetRowColumn(fileNameOut, 1, 4)
if ("" == test) :
    print("Remove Column from END, CSV NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Column from END, CSV NO HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=COMMA)
# end test
PTX.removeColumn(fileNameOut, "0", headers=False)
test = GetRowColumn(fileNameOut, 1, 1)
if ("start1" != test) :
    print("Remove Column from START, CSV NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Column from START, CSV NO HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=COMMA)
# end test
PTX.removeRows(fileNameOut, "1", "pipe", headers=False)
test = GetRowColumn(fileNameOut, 3, 2)
if ("pipe" != test) :
    print("Remove Row by ColValue, CSV NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Row by ColValue, CSV NO HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=COMMA)
# end test

#################################################
# CSV file, has non-ascii characters, With header
#################################################
fileNameIn = os.path.join(dirIn,  "TestBadCharsHeader.csv")
# copy to DBFile
fileNameOut = os.path.join(dirOut,  "TestBadCharsHeader_DBFile.csv")
shutil.copy(fileNameIn, fileNameOut)
PTX.removeNonAscii(fileNameOut, PTX.COMMA)
test = GetRowColumn(fileNameOut, 1, 1)
if ("test" == test) :
    print("Remove Ascii, from CSV WITH HEADER, colName check " + "SUCCESS")
else :
    print("Remove Ascii, from CSV WITH HEADER, colName check " + "FAIL")
    PrintRowColumns(fileNameOut, delim=COMMA)
# end test
test = GetRowColumn(fileNameOut, 2, 1)
if ("Dj vu" == test) :
    print("Remove Ascii, from CSV WITH HEADER, colValue check " + "SUCCESS")
else :
    print("Remove Ascii, from CSV WITH HEADER, colValue check " + "FAIL")
    PrintRowColumns(fileNameOut, delim=COMMA)
# end test

PTX.addColumn(fileNameOut, "ColEnd1", "End1")
test = GetRowColumn(fileNameOut, 1, 3)
if ("ColEnd1" == test) :
    print("Add Column to END, from CSV WITH HEADER, colName Test " + "SUCCESS")
else :
    print("Add Column to END, from CSV WITH HEADER, colName Test " + "FAIL")
    PrintRowColumns(fileNameOut, delim=COMMA)
# end test
test = GetRowColumn(fileNameOut, 2, 3)
if ("End1" == test) :
    print("Add Column to END, CSV WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Add Column to END, CSV WITH HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=COMMA)
# end test

PTX.addColumn(fileNameOut, "Colstart1", "start1", PTX.COL_BEGIN)
test = GetRowColumn(fileNameOut, 1, 1)
if ("Colstart1" == test) :
    print("Add Column to START, CSV WITH HEADER, colNameTest " + "SUCCESS")
else :
    print("Add Column to START, CSV WITH HEADER, colNameTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=COMMA)
# end test
test = GetRowColumn(fileNameOut, 2, 1)
if ("start1" == test) :
    print("Add Column to START, CSV WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Add Column to START, CSV WITH HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=COMMA) 
# end test
PTX.removeColumn(fileNameOut, "ColEnd1")
test = GetRowColumn(fileNameOut, 1, 4)
if ("" == test) :
    print("Remove Column from END, CSV WITH HEADER, colNameTest " + "SUCCESS")
else :
    print("Remove Column from END, CSV WITH HEADER, colNameTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=COMMA)
# end test
test = GetRowColumn(fileNameOut, 2, 4)
if ("" == test) :
    print("Remove Column from END, CSV WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Column from END, CSV WITH HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=COMMA)
# end test
PTX.removeColumn(fileNameOut, "Colstart1")
test = GetRowColumn(fileNameOut, 1, 1)
if ("Colstart1" != test) :
    print("Remove Column from START, CSV WITH HEADER, colNameTest " + "SUCCESS")
else :
    print("Remove Column from START, CSV WITH HEADER, colNameTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=COMMA)
# end test
test = GetRowColumn(fileNameOut, 2, 1)
if ("start1" != test) :
    print("Remove Column from START, CSV WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Column from START, CSV WITH HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=COMMA)
# end test
PTX.removeRows(fileNameOut, "desc", "pipe")
test = GetRowColumn(fileNameOut, 4, 2)
if ("pipe" != test) :
    print("Remove Row by ColValue, CSV WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Row by ColValue, CSV WITH HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=COMMA)
# end test
#################################################
# TAB file, has non-ascii characters, no header
#################################################
fileNameIn = os.path.join(dirIn,  "TestBadChars.txt")
# copy to DBFile
fileNameOut = os.path.join(dirOut,  "TestBadChars_DBFile.txt")
shutil.copy(fileNameIn, fileNameOut)
PTX.removeNonAscii(fileNameOut, TAB, False)
test = GetRowColumn(fileNameOut, 1, 1, delim=TAB)
if ("Dj vu" == test) :
    print("Remove Ascii from TAB NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Ascii from TAB NO HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=TAB) 
# end test
PTX.addColumn(fileNameOut, "", "End1", headersIn=False, delim=TAB)
test = GetRowColumn(fileNameOut, 1, 3, delim=TAB)
if (test.startswith("End1")) :
    print("Add Column to END, TAB NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Add Column to END, TAB NO HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=TAB)
# end test
PTX.addColumn(fileNameOut, "Colstart1", "start1", headersIn=False, delim=TAB, colLocation=PTX.COL_BEGIN)
test = GetRowColumn(fileNameOut, 1, 1, delim=TAB)
if ("start1" == test) :
    print("Add Column to START, TAB NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Add Column to START, TAB NO HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=TAB) 
# end test
PTX.removeColumn(fileNameOut, "3", headers=False, delim=TAB)
test = GetRowColumn(fileNameOut, 1, 4)
if ("" == test) :
    print("Remove Column from END, TAB NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Column from END, TAB NO HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=TAB)
# end test
PTX.removeColumn(fileNameOut, "0", headers=False, delim=TAB)
test = GetRowColumn(fileNameOut, 1, 1)
if ("start1" != test) :
    print("Remove Column from START, TAB NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Column from START, TAB NO HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=TAB)
# end test
PTX.removeRows(fileNameOut, "1", "pipe", headers=False, delim=TAB)
test = GetRowColumn(fileNameOut, 3, 2, delim=TAB)
if ("pipe" != test) :
    print("Remove Row by ColValue, TAB NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Row by ColValue, TAB NO HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=TAB)
# end test
#################################################
# TAB file, has non-ascii characters, with header
#################################################
fileNameIn = os.path.join(dirIn,  "TestBadCharsHeader.txt")
# copy to DBFile
fileNameOut = os.path.join(dirOut,  "TestBadCharsHeader_DBFile.txt")
shutil.copy(fileNameIn, fileNameOut)
PTX.removeNonAscii(fileNameOut, delim=TAB)
test = GetRowColumn(fileNameOut, 1, 1,delim=TAB)
if ("test" == test) :
    print("Remove Ascii, TAB WITH HEADER, colNameTest " + "SUCCESS")
else :
    print("Remove Ascii, TAB WITH HEADER, colNameTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=TAB) 
# end test
test = GetRowColumn(fileNameOut, 2, 1,delim=TAB)
if ("Dj vu" == test) :
    print("Remove Ascii, from TAB WITH HEADER, colValue check " + "SUCCESS")
else :
    print("Remove Ascii, from TAB WITH HEADER, colValue check " + "FAIL")
    PrintRowColumns(fileNameOut, delim=TAB) 
# end test

PTX.addColumn(fileNameOut, "ColEnd1", "End1",delim=TAB)
test = GetRowColumn(fileNameOut, 1, 3,delim=TAB)
if ("ColEnd1" == test) :
    print("Add Column to END, TAB WITH HEADER, colNameTest " + "SUCCESS")
else :
    print("Add Column to END,  TAB WITH HEADER, colNameTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=TAB) 
# end test
test = GetRowColumn(fileNameOut, 2, 3,delim=TAB)
if ("End1" == test) :
    print("Add Column to END, TAB WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Add Column to END, TAB WITH HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=TAB) 
# end test

PTX.addColumn(fileNameOut, "Colstart1", "start1", colLocation=PTX.COL_BEGIN, delim=TAB)
test = GetRowColumn(fileNameOut, 1, 1,delim=TAB)
if ("Colstart1" == test) :
    print("Add Column to START, TAB WITH HEADER, colNameTest " + "SUCCESS")
else :
    print("Add Column to START,  TAB WITH HEADER, colNameTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=TAB) 
# end test
test = GetRowColumn(fileNameOut, 2, 1,delim=TAB)
if ("start1" == test) :
    print("Add Column to START, TAB WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Add Column to START, TAB WITH HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=TAB) 
# end test
PTX.removeColumn(fileNameOut, "ColEnd1", delim=TAB)
test = GetRowColumn(fileNameOut, 1, 4, delim=TAB)
if ("" == test) :
    print("Remove Column from END, TAB WITH HEADER, colNameTest " + "SUCCESS")
else :
    print("Remove Column from END, TAB WITH HEADER, colNameTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=TAB)
# end test
test = GetRowColumn(fileNameOut, 2, 4, delim=TAB)
if ("" == test) :
    print("Remove Column from END, TAB WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Column from END, TAB WITH HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=TAB)
# end test
PTX.removeColumn(fileNameOut, "Colstart1", delim=TAB)
test = GetRowColumn(fileNameOut, 1, 1, delim=TAB)
if ("Colstart1" != test) :
    print("Remove Column from START, TAB WITH HEADER, colNameTest " + "SUCCESS")
else :
    print("Remove Column from START, TAB WITH HEADER, colNameTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=TAB)
# end test
test = GetRowColumn(fileNameOut, 2, 1, delim=TAB)
if ("start1" != test) :
    print("Remove Column from START, TAB WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Column from START, TAB WITH HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=TAB)
# end test
PTX.removeRows(fileNameOut, "desc", "pipe", delim=TAB)
test = GetRowColumn(fileNameOut, 4, 2, delim=TAB)
if ("pipe" != test) :
    print("Remove Row by ColValue, TAB WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Row by ColValue, TAB WITH HEADER, colValueTest " + "FAIL")
    PrintRowColumns(fileNameOut, delim=TAB)
# end test