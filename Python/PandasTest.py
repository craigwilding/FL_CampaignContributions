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

dictRenameColumns = {
    "desc": "description"
}
listNullIntColHeader = ["test"]
listNullIntColIndex = [0]
listNullStrColHeader = ["desc"]
listNullStrColIndex = [1]

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
print("**************** CSV NO HEADER *******************")
fileNameIn = os.path.join(dirIn,  "TestBadChars.csv")
# copy to DBFile
fileNameOut = os.path.join(dirOut,  "TestBadChars_DBFile.csv")
shutil.copy(fileNameIn, fileNameOut)
csvNoHead = PTX.PandasTransform(fileNameOut, delim=COMMA, headers=False)
csvNoHead.removeNonAscii()
test = csvNoHead.TestRowColumn( 1, 1)
if ("Dj vu" == test) :
    print("Remove Ascii from CSV NO HEADER " + "SUCCESS")
else :
    print("Remove Ascii from CSV NO HEADER " + "FAIL")
    csvNoHead.PrintRowColumns()
# end test
csvNoHead.setNullValues(listNullIntColIndex,"0")
test = csvNoHead.TestRowColumn( 5, 1)
if ("0" == test) :
    print("Set Null Int, CSV NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Set Null Int, CSV NO HEADER, colValueTest " + "FAIL")
    print("test = [" + test + "]")
    csvNoHead.PrintRowColumns()
# end test
csvNoHead.setNullValues(listNullStrColIndex, "NULL")
test = csvNoHead.TestRowColumn( 6, 2)
if ("NULL" == test) :
    print("Set Null Str, CSV NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Set Null Str, CSV NO HEADER, colValueTest " + "FAIL")
    csvNoHead.PrintRowColumns()
# end test
csvNoHead.addColumn("", "End1")
test = csvNoHead.TestRowColumn( 1, 3)
if ("End1" == test) :
    print("Add Column to END, CSV NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Add Column to END, CSV NO HEADER, colValueTest " + "FAIL")
    csvNoHead.PrintRowColumns()
# end test
csvNoHead.addColumn("Colstart1", "start1", colLocation=PTX.COL_BEGIN)
test = csvNoHead.TestRowColumn( 1, 1)
if ("start1" == test) :
    print("Add Column to START, CSV NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Add Column to START, CSV NO HEADER, colValueTest " + "FAIL")
    csvNoHead.PrintRowColumns()
# end test
csvNoHead.removeColumn("3")
test = csvNoHead.TestRowColumn( 1, 4)
if ("" == test) :
    print("Remove Column from END, CSV NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Column from END, CSV NO HEADER, colValueTest " + "FAIL")
    csvNoHead.PrintRowColumns()
# end test
csvNoHead.removeColumn("0")
test = csvNoHead.TestRowColumn( 1, 1)
if ("start1" != test) :
    print("Remove Column from START, CSV NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Column from START, CSV NO HEADER, colValueTest " + "FAIL")
    csvNoHead.PrintRowColumns()
# end test
csvNoHead.removeRows("1", "pipe")
test = csvNoHead.TestRowColumn( 3, 2)
if ("pipe" != test) :
    print("Remove Row by ColValue, CSV NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Row by ColValue, CSV NO HEADER, colValueTest " + "FAIL")
    csvNoHead.PrintRowColumns()
# end test


#################################################
# CSV file, has non-ascii characters, With header
#################################################
print("**************** CSV WITH HEADER *******************")
fileNameIn = os.path.join(dirIn,  "TestBadCharsHeader.csv")
# copy to DBFile
fileNameOut = os.path.join(dirOut,  "TestBadCharsHeader_DBFile.csv")
shutil.copy(fileNameIn, fileNameOut)
csvWithHead = PTX.PandasTransform(fileNameOut)
csvWithHead.removeNonAscii()
test = csvWithHead.TestRowColumn( 1, 1)
if ("test" == test) :
    print("Remove Ascii, from CSV WITH HEADER, colName check " + "SUCCESS")
else :
    print("Remove Ascii, from CSV WITH HEADER, colName check " + "FAIL")
    csvWithHead.PrintRowColumns()
# end test
test = csvWithHead.TestRowColumn( 2, 1)
if ("Dj vu" == test) :
    print("Remove Ascii, from CSV WITH HEADER, colValue check " + "SUCCESS")
else :
    print("Remove Ascii, from CSV WITH HEADER, colValue check " + "FAIL")
    csvWithHead.PrintRowColumns()
# end test
csvWithHead.setNullValues(listNullIntColHeader, "0")
test = csvWithHead.TestRowColumn( 6, 1)
if ("0" == test) :
    print("Set Null Int, CSV WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Set Null Int, CSV WITH HEADER, colValueTest " + "FAIL")
    csvWithHead.PrintRowColumns()
# end test
csvWithHead.setNullValues(listNullStrColHeader, "NULL")
test = csvWithHead.TestRowColumn( 7, 2)
if ("NULL" == test) :
    print("Set Null Str, CSV WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Set Null Str, CSV WITH HEADER, colValueTest " + "FAIL")
    csvWithHead.PrintRowColumns()
# end test
csvWithHead.addColumn("ColEnd1", "End1")
test = csvWithHead.TestRowColumn( 1, 3)
if ("ColEnd1" == test) :
    print("Add Column to END, from CSV WITH HEADER, colName Test " + "SUCCESS")
else :
    print("Add Column to END, from CSV WITH HEADER, colName Test " + "FAIL")
    csvWithHead.PrintRowColumns()
# end test
test = csvWithHead.TestRowColumn( 2, 3)
if ("End1" == test) :
    print("Add Column to END, CSV WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Add Column to END, CSV WITH HEADER, colValueTest " + "FAIL")
    csvWithHead.PrintRowColumns()
# end test
csvWithHead.addColumn("Colstart1", "start1", PTX.COL_BEGIN)
test = csvWithHead.TestRowColumn( 1, 1)
if ("Colstart1" == test) :
    print("Add Column to START, CSV WITH HEADER, colNameTest " + "SUCCESS")
else :
    print("Add Column to START, CSV WITH HEADER, colNameTest " + "FAIL")
    csvWithHead.PrintRowColumns()
# end test
test = csvWithHead.TestRowColumn( 2, 1)
if ("start1" == test) :
    print("Add Column to START, CSV WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Add Column to START, CSV WITH HEADER, colValueTest " + "FAIL")
    csvWithHead.PrintRowColumns() 
# end test
csvWithHead.removeColumn("ColEnd1")
test = csvWithHead.TestRowColumn( 1, 4)
if ("" == test) :
    print("Remove Column from END, CSV WITH HEADER, colNameTest " + "SUCCESS")
else :
    print("Remove Column from END, CSV WITH HEADER, colNameTest " + "FAIL")
    csvWithHead.PrintRowColumns()
# end test
test = csvWithHead.TestRowColumn( 2, 4)
if ("" == test) :
    print("Remove Column from END, CSV WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Column from END, CSV WITH HEADER, colValueTest " + "FAIL")
    csvWithHead.PrintRowColumns()
# end test
csvWithHead.removeColumn("Colstart1")
test = csvWithHead.TestRowColumn( 1, 1)
if ("Colstart1" != test) :
    print("Remove Column from START, CSV WITH HEADER, colNameTest " + "SUCCESS")
else :
    print("Remove Column from START, CSV WITH HEADER, colNameTest " + "FAIL")
    csvWithHead.PrintRowColumns()
# end test
test = csvWithHead.TestRowColumn( 2, 1)
if ("start1" != test) :
    print("Remove Column from START, CSV WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Column from START, CSV WITH HEADER, colValueTest " + "FAIL")
    csvWithHead.PrintRowColumns()
# end test
csvWithHead.renameColumn(dictRenameColumns)
test = csvWithHead.TestRowColumn( 1, 2)
if ("description" == test) :
    print("Rename Column, CSV WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Rename Column, CSV WITH HEADER, colValueTest " + "FAIL")
    csvWithHead.PrintRowColumns()
# end test
#################################################
# TAB file, has non-ascii characters, no header
#################################################
print("**************** TAB NO HEADER *******************")
fileNameIn = os.path.join(dirIn,  "TestBadChars.txt")
# copy to DBFile
fileNameOut = os.path.join(dirOut,  "TestBadChars_DBFile.txt")
shutil.copy(fileNameIn, fileNameOut)
tabNoHead = PTX.PandasTransform(fileNameOut, delim=TAB, headers=False)
tabNoHead.removeNonAscii()
test = tabNoHead.TestRowColumn( 1, 1)
if ("Dj vu" == test) :
    print("Remove Ascii from TAB NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Ascii from TAB NO HEADER, colValueTest " + "FAIL")
    tabNoHead.PrintRowColumns() 
# end test
tabNoHead.setNullValues(listNullIntColIndex, "0")
test = tabNoHead.TestRowColumn( 5, 1)
if ("0" == test) :
    print("Set Null Int, TAB NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Set Null Int, TAB NO HEADER, colValueTest " + "FAIL")
    tabNoHead.PrintRowColumns()
# end test
tabNoHead.setNullValues(listNullStrColIndex, "NULL")
test = tabNoHead.TestRowColumn( 6, 2)
if ("NULL" == test) :
    print("Set Null Str, TAB NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Set Null Str, TAB NO HEADER, colValueTest " + "FAIL")
    tabNoHead.PrintRowColumns()
# end test
tabNoHead.addColumn("", "End1")
test = tabNoHead.TestRowColumn( 1, 3)
if (test.startswith("End1")) :
    print("Add Column to END, TAB NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Add Column to END, TAB NO HEADER, colValueTest " + "FAIL")
    tabNoHead.PrintRowColumns() 
# end test
tabNoHead.addColumn("Colstart1", "start1", colLocation=PTX.COL_BEGIN)
test = tabNoHead.TestRowColumn( 1, 1)
if ("start1" == test) :
    print("Add Column to START, TAB NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Add Column to START, TAB NO HEADER, colValueTest " + "FAIL")
    tabNoHead.PrintRowColumns() 
# end test
tabNoHead.removeColumn("3")
test = tabNoHead.TestRowColumn( 1, 4)
if ("" == test) :
    print("Remove Column from END, TAB NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Column from END, TAB NO HEADER, colValueTest " + "FAIL")
    tabNoHead.PrintRowColumns() 
# end test
tabNoHead.removeColumn("0")
test = tabNoHead.TestRowColumn( 1, 1)
if ("start1" != test) :
    print("Remove Column from START, TAB NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Column from START, TAB NO HEADER, colValueTest " + "FAIL")
    tabNoHead.PrintRowColumns() 
# end test
tabNoHead.removeRows("1", "pipe")
test = tabNoHead.TestRowColumn( 3, 2)
if ("pipe" != test) :
    print("Remove Row by ColValue, TAB NO HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Row by ColValue, TAB NO HEADER, colValueTest " + "FAIL")
    tabNoHead.PrintRowColumns() 
# end test

#################################################
# TAB file, has non-ascii characters, with header
#################################################
print("**************** TAB WITH HEADER *******************")
fileNameIn = os.path.join(dirIn,  "TestBadCharsHeader.txt")
# copy to DBFile
fileNameOut = os.path.join(dirOut,  "TestBadCharsHeader_DBFile.txt")
shutil.copy(fileNameIn, fileNameOut)
tabWithHead = PTX.PandasTransform(fileNameOut, delim=TAB)
tabWithHead.removeNonAscii()
test = tabWithHead.TestRowColumn( 1, 1)
if ("test" == test) :
    print("Remove Ascii, TAB WITH HEADER, colNameTest " + "SUCCESS")
else :
    print("Remove Ascii, TAB WITH HEADER, colNameTest " + "FAIL")
    tabWithHead.PrintRowColumns() 
# end test
test = tabWithHead.TestRowColumn( 2, 1)
if ("Dj vu" == test) :
    print("Remove Ascii, from TAB WITH HEADER, colValue check " + "SUCCESS")
else :
    print("Remove Ascii, from TAB WITH HEADER, colValue check " + "FAIL")
    tabWithHead.PrintRowColumns() 
# end test
tabWithHead.setNullValues(listNullIntColHeader,"0")
test = tabWithHead.TestRowColumn( 6, 1)
if ("0" == test) :
    print("Set Null Int, TAB WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Set Null Int, TAB WITH HEADER, colValueTest " + "FAIL")
    tabWithHead.PrintRowColumns()
# end test
tabWithHead.setNullValues(listNullStrColHeader, "NULL")
test = tabWithHead.TestRowColumn( 7, 2)
if ("NULL" == test) :
    print("Set Null Str, TAB WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Set Null Str, TAB WITH HEADER, colValueTest " + "FAIL")
    tabWithHead.PrintRowColumns()
# end test
tabWithHead.addColumn("ColEnd1", "End1")
test = tabWithHead.TestRowColumn( 1, 3)
if ("ColEnd1" == test) :
    print("Add Column to END, TAB WITH HEADER, colNameTest " + "SUCCESS")
else :
    print("Add Column to END,  TAB WITH HEADER, colNameTest " + "FAIL")
    tabWithHead.PrintRowColumns()  
# end test
test = tabWithHead.TestRowColumn( 2, 3)
if ("End1" == test) :
    print("Add Column to END, TAB WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Add Column to END, TAB WITH HEADER, colValueTest " + "FAIL")
    tabWithHead.PrintRowColumns() 
# end test

tabWithHead.addColumn("Colstart1", "start1", colLocation=PTX.COL_BEGIN)
test = tabWithHead.TestRowColumn( 1, 1)
if ("Colstart1" == test) :
    print("Add Column to START, TAB WITH HEADER, colNameTest " + "SUCCESS")
else :
    print("Add Column to START,  TAB WITH HEADER, colNameTest " + "FAIL")
    tabWithHead.PrintRowColumns() 
# end test
test = tabWithHead.TestRowColumn( 2, 1)
if ("start1" == test) :
    print("Add Column to START, TAB WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Add Column to START, TAB WITH HEADER, colValueTest " + "FAIL")
    tabWithHead.PrintRowColumns() 
# end test
tabWithHead.removeColumn("ColEnd1")
test = tabWithHead.TestRowColumn( 1, 4)
if ("" == test) :
    print("Remove Column from END, TAB WITH HEADER, colNameTest " + "SUCCESS")
else :
    print("Remove Column from END, TAB WITH HEADER, colNameTest " + "FAIL")
    tabWithHead.PrintRowColumns() 
# end test
test = tabWithHead.TestRowColumn( 2, 4)
if ("" == test) :
    print("Remove Column from END, TAB WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Column from END, TAB WITH HEADER, colValueTest " + "FAIL")
    tabWithHead.PrintRowColumns() 
# end test
tabWithHead.removeColumn("Colstart1")
test = tabWithHead.TestRowColumn( 1, 1)
if ("Colstart1" != test) :
    print("Remove Column from START, TAB WITH HEADER, colNameTest " + "SUCCESS")
else :
    print("Remove Column from START, TAB WITH HEADER, colNameTest " + "FAIL")
    tabWithHead.PrintRowColumns() 
# end test
test = tabWithHead.TestRowColumn( 2, 1)
if ("start1" != test) :
    print("Remove Column from START, TAB WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Column from START, TAB WITH HEADER, colValueTest " + "FAIL")
    tabWithHead.PrintRowColumns() 
# end test
tabWithHead.removeRows("desc", "pipe")
test = tabWithHead.TestRowColumn( 4, 2)
if ("pipe" != test) :
    print("Remove Row by ColValue, TAB WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Remove Row by ColValue, TAB WITH HEADER, colValueTest " + "FAIL")
    tabWithHead.PrintRowColumns() 
# end test
tabWithHead.renameColumn(dictRenameColumns)
test = tabWithHead.TestRowColumn( 1, 2)
if ("description" == test) :
    print("Rename Column, TAB WITH HEADER, colValueTest " + "SUCCESS")
else :
    print("Rename Column, TAB WITH HEADER, colValueTest " + "FAIL")
    tabWithHead.PrintRowColumns()
# end test