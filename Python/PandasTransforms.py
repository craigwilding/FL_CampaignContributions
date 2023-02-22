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
# indicates whether to add a column to beginning or end
COL_BEGIN = 0
COL_END = -1

class PandasTransform :
    ###########################################################
    # PandasTransform.Init()
    # Assign the file name, delimiter and whether the file has column headers or not
    # This allows the transforms to adjust to the type of file
    # rather than having to pass in these paramaters to each function
    #
    # fileNameIn - name of the file.  All transforms will be written back to this file
    # delim - The file delimiter, COMMA is the default.  It assumes CSV files
    #         Set to TAB for tab delimited text file
    # headers - True/False indicates whether the file contains headers or not
    ###########################################################
    def __init__(self, fileNameIn, delim=COMMA, headers=True):
        self.fileNameIn = fileNameIn
        self.delim = delim
        self.headers = headers
    # end init

    ############################################
    # Remove Non-Ascii 
    # Remove non utf8 characters that break loading into the database
    # This replaces the fileNameIn with the converted file.
    ############################################
    def removeNonAscii(self) :
        headerVal=0
        if (self.headers != True) :
            headerVal = None
        # end headerVal
        fileNameOut = self.fileNameIn.replace(".", "_asciiTest.")

        # try reading as iso-8859-1 to allow non-asciicharacters
        df = pandas.read_csv(self.fileNameIn,delimiter=self.delim, encoding="iso-8859-1", header=headerVal)

        for col in df.columns:
            # convert non-english characters.
            df[col].replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)
        # end for columns

        # write to temp file
        df.to_csv(fileNameOut, encoding='utf-8', index=False, sep=self.delim, header=self.headers)
        # replace in File with temp file
        shutil.move(fileNameOut, self.fileNameIn)
    # end removeNonAscii

    ############################################
    # Add Column 
    # Add a column to the file
    # This replaces the fileNameIn with the converted file.
    ############################################

    def addColumn(self, newColName, defaultValue, colLocation=COL_END) :

        headerVal=0
        if (self.headers != True) :
            headerVal = None
        # end headerVal
        fileNameOut = self.fileNameIn.replace(".", "_addColumn" + newColName + ".")

        # Read as pandas data frame
        df = pandas.read_csv(self.fileNameIn,sep=self.delim,header=headerVal,index_col=False)
            
        #check if has column headers already
        topline = str(df.head(1))
        if (topline.find(newColName) < 0) or (self.headers == False) :

            # add the column with default value.
            if (self.headers == True) :
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
        df.to_csv(fileNameOut, encoding='utf-8', index=False, header=self.headers, sep=self.delim)
        # replace in File with temp file
        shutil.move(fileNameOut, self.fileNameIn)
    # end addColumn

    ############################################
    # Remove Column 
    # Remove a column from the file
    # If headers=False, then colName must be the column index to remove
    # This replaces the fileNameIn with the converted file.
    ############################################
    def removeColumn(self, colName) :

        headerVal=0
        if (self.headers != True) :
            headerVal = None
        # end headerVal

        fileNameOut = self.fileNameIn.replace(".", "_remColumn.")

        # Read as pandas data frame
        df = pandas.read_csv(self.fileNameIn,sep=self.delim,header=headerVal,index_col=False)
            
        #check if has column exists already
        topline = str(df.head(1))
        if ((topline.find(colName) > 0) or (self.headers == False)) :

            # Remove the column
            if (self.headers == True) :
                df.pop(colName)
            else :
                ix = int(colName)
                df.drop(df.columns[ix], axis=1,inplace=True)
            # end if header
        else :
            print("column did not exists: " + colName)
        # end if office

        # write to temp file
        df.to_csv(fileNameOut, encoding='utf-8', index=False, header=self.headers, sep=self.delim)
        # replace in File with temp file
        shutil.move(fileNameOut, self.fileNameIn)
    # end removeColumn

    ############################################
    # Remove Rows 
    # Remove rows where it matches a column value
    # If headers=False, then colName must be the column index to remove
    # This replaces the fileNameIn with the converted file.
    ############################################
    def removeRows(self, colName, colValue) :

        headerVal=0
        if (self.headers != True) :
            headerVal = None
        # end headerVal

        fileNameOut = self.fileNameIn.replace(".", "_remRow.")

        # Read as pandas data frame
        df = pandas.read_csv(self.fileNameIn,sep=self.delim,header=headerVal,index_col=False)
            
        #check if has column exists already
        topline = str(df.head(1))
        if ((topline.find(colName) > 0) or (self.headers == False)) :

            listValues = []
            listValues.append(colValue)

            # Remove the column
            if (self.headers == True) :
                df = df[~df[colName].isin(listValues)]
            else :
                ix = int(colName)   
                df = df[~df[ix].isin(listValues)]
            # end if header
        else :
            print("column did not exists: " + colName)
        # end if office

        # write to temp file
        df.to_csv(fileNameOut, encoding='utf-8', index=False, header=self.headers, sep=self.delim)
        # replace in File with temp file
        shutil.move(fileNameOut, self.fileNameIn)
    # end removeRows

    ############################################
    # Rename Column 
    # Rename a column from the file
    # The column(s) to be changed must be passed in as a dictionary
    # dictRenameColumns - (key = oldName, value = new name)
    ############################################
    def renameColumn(self, dictRenameColumns) :

        headerVal=0
        if (self.headers != True) :
            return  # skip if no column headers to rename!!!
        # end headerVal

        fileNameOut = self.fileNameIn.replace(".", "_renameColumn.")

        # Read as pandas data frame
        df = pandas.read_csv(self.fileNameIn,sep=self.delim,header=headerVal,index_col=False)
            
        #check if has column exists already
        df.rename(columns=dictRenameColumns, inplace=True)

        # write to temp file
        df.to_csv(fileNameOut, encoding='utf-8', index=False, header=self.headers, sep=self.delim)
        # replace in File with temp file
        shutil.move(fileNameOut, self.fileNameIn)
    # end renameColumn

    ############################################
    # SetNullValues() 
    # Set all missing values on a column to a given value
    # Params 
    # listColumns - a list of columns to check for null values
    # nullValue - the value to set the columns to.
    #
    # Notes:  This can be used in multiple ways:
    # + Set all integer or float files to 0 instead of blank
    # + Set 'NULL' as the common null value, then use that in the DB Load command NULL as 'NULL'
    ############################################

    def setNullValues(self, listColumns, nullValue="") :

        headerVal=0
        if (self.headers != True) :
            headerVal = None
        # end headerVal
        fileNameOut = self.fileNameIn.replace(".", "_setnull" + ".")

        # Read as pandas data frame
        df = pandas.read_csv(self.fileNameIn,sep=self.delim,header=headerVal,index_col=False)
            
        #check if has column headers already
        for colName in listColumns :

            df[colName].fillna(nullValue, inplace=True)
        # end for

        # write to temp file
        df.to_csv(fileNameOut, encoding='utf-8', index=False, header=self.headers, sep=self.delim)
        # replace in File with temp file
        shutil.move(fileNameOut, self.fileNameIn)
    # end SetNullValuesAsInt


    def TestRowColumn(self, rowNum, colNum) :
        # this is used to test the results
        # it counts the header as a row number if there is one.
        testVal = ""
        fileIn = open(self.fileNameIn, encoding='utf-8')
        rowCount = 0
        for line in fileIn :
            rowCount += 1
            if (rowNum != rowCount) :
                continue

            columns = line.replace(EOL,"").split(self.delim)
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
    # end TestRowColumn

    def PrintRowColumns(self) :
        # this is used to print the testresults
        fileIn = open(self.fileNameIn, encoding='utf-8')
        rowCount = 0
        for line in fileIn :
            rowCount += 1

            columns = line.replace(EOL,"").split(self.delim)
            colCount = 0
            for col in columns :
                colCount += 1
                print("Row: " + str(rowCount) + " Col: " + str(colCount) + " value: " + str(col))
            # end for columns
        # end for each line
        fileIn.close()
        del fileIn

    # end PrintRowColumns

# end class PandasTransform