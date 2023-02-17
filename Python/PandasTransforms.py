import os
import shutil
import pandas

################################################
# Pandas Transforms
# This file contains common data transformations 
# used to transform data before loading to a database.
#################################################

TAB = "\t"
EOL = '\n'
COMMA = ','
QUOTE = '"'
SINGLE_QUOTE = "'"



############################################
# Remove Non-Ascii 
# Remove non utf8 characters that break loading into the database
# This replaces the fileNameIn with the converted file.
############################################
def removeNonAscii(fileNameIn, delim=COMMA,headersIn=True) :

    headerVal=0
    if (headersIn != True) :
        headerVal = None
    # end headerVal
    fileNameOut = fileNameIn.replace(".", "_asciiTest.")

    # try reading as iso-8859-1 to allow non-asciicharacters
    df = pandas.read_csv(fileNameIn,delimiter=delim, encoding="iso-8859-1", header=headerVal)

    for col in df.columns:
        # convert non-english characters.
        df[col].replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)
    # end for columns

    # write to temp file
    df.to_csv(fileNameOut, encoding='utf-8', index=False, sep=delim, header=headersIn)
    # replace in File with temp file
    shutil.move(fileNameOut, fileNameIn)
# end removeNonAscii

############################################
# Add Column 
# Add a column to the file
# This replaces the fileNameIn with the converted file.
############################################
# indicates whether to add a column to beginning or end
COL_BEGIN = 0
COL_END = -1
def addColumn(fileNameIn, newColName, defaultValue, colLocation=COL_END,delim=COMMA,headersIn=True) :

    headerVal=0
    if (headersIn != True) :
        headerVal = None
    # end headerVal
    fileNameOut = fileNameIn.replace(".", "_addColumn" + newColName + ".")

    # Read as pandas data frame
    df = pandas.read_csv(fileNameIn,sep=delim,header=headerVal,index_col=False)
        
    #check if has column headers already
    topline = str(df.head(1))
    if (topline.find(newColName) < 0) or (headersIn == False) :

        # add the column with default value.
        if (headersIn == True) :
            if (COL_BEGIN == colLocation) :
                df.insert(0,newColName,'')
            # end insert at beginning
            df[newColName] = defaultValue
        else :
            if (COL_BEGIN == colLocation) :
                df.insert(0,'',defaultValue)
            else :
                df[len(df.columns)] = defaultValue
            # end no header
        # end if header
    else :
        print("column already exists: " + newColName)
    # end if office

    # write to temp file
    df.to_csv(fileNameOut, encoding='utf-8', index=False, header=headersIn, sep=delim)
    # replace in File with temp file
    shutil.move(fileNameOut, fileNameIn)
# end addColumn

############################################
# Remove Column 
# Remove a column from the file
# If headers=False, then colName must be the column index to remove
# This replaces the fileNameIn with the converted file.
############################################
def removeColumn(fileNameIn, colName, delim=COMMA, headers=True) :

    headerVal=0
    if (headers != True) :
        headerVal = None
    # end headerVal

    fileNameOut = fileNameIn.replace(".", "_remColumn.")

    # Read as pandas data frame
    df = pandas.read_csv(fileNameIn,sep=delim,header=headerVal,index_col=False)
        
    #check if has column exists already
    topline = str(df.head(1))
    if ((topline.find(colName) > 0) or (headers == False)) :

        # Remove the column
        if (headers == True) :
            df.pop(colName)
        else :
            ix = int(colName)
            df.drop(df.columns[ix], axis=1,inplace=True)
        # end if header
    else :
        print("column did not exists: " + colName)
    # end if office

    # write to temp file
    df.to_csv(fileNameOut, encoding='utf-8', index=False, header=headers, sep=delim)
    # replace in File with temp file
    shutil.move(fileNameOut, fileNameIn)
# end removeColumn

############################################
# Remove Rows 
# Remove rows where it matches a column value
# If headers=False, then colName must be the column index to remove
# This replaces the fileNameIn with the converted file.
############################################
def removeRows(fileNameIn, colName, colValue, delim=COMMA, headers=True) :

    headerVal=0
    if (headers != True) :
        headerVal = None
    # end headerVal

    fileNameOut = fileNameIn.replace(".", "_remRow.")

    # Read as pandas data frame
    df = pandas.read_csv(fileNameIn,sep=delim,header=headerVal,index_col=False)
        
    #check if has column exists already
    topline = str(df.head(1))
    if ((topline.find(colName) > 0) or (headers == False)) :

        listValues = []
        listValues.append(colValue)

        # Remove the column
        if (headers == True) :
            df = df[~df[colName].isin(listValues)]
        else :
            ix = int(colName)   
            df = df[~df[ix].isin(listValues)]
        # end if header
    else :
        print("column did not exists: " + colName)
    # end if office

    # write to temp file
    df.to_csv(fileNameOut, encoding='utf-8', index=False, header=headers, sep=delim)
    # replace in File with temp file
    shutil.move(fileNameOut, fileNameIn)
# end removeRows