######################################
# Common SQL commands
######################################
import psycopg2
import os

TAB = "\t"
COMMA = ','
SINGLE_QT = "'"
SQL_END = ";"

######################################
# SQL Connection
######################################
def Connect() :
     return psycopg2.connect( host='localhost', user='postgres', password='postgres', dbname='postgres')
# end Connect()

def Exec(connection, sql) :
    with connection.cursor() as cursor:
        print(sql)
        cursor.execute(sql)
    # end with cursor
# end Exec

######################################
# INDEXES
# Enforces a standard naming convention
######################################
def DropIndex(connection, table, columnName) :
    sql = "DROP INDEX IF EXISTS "
    sql += table + "_" + columnName + "_idx;"
    Exec(connection, sql)
# end DropIndex

def CreateIndex(connection, table, columnName) :
    sql = "CREATE INDEX IF NOT EXISTS "
    sql += table + "_" + columnName + "_idx"
    sql += " ON " + table 
    # sql += " USING btree"
    sql += " (" + columnName + " ASC NULLS LAST)"
    sql += ";"
    Exec(connection, sql)
# end CreateIndex

######################################
######################################
######################################
# TABLES
# Common Delete, Load, Select methods
######################################
######################################
######################################

######################################
# Delete Where
# Use to delete old rows before loading new ones
# Use where clause to select rows to be deleted
######################################
def DeleteWhere(connection, table, whereSql="") :
    sql = "DELETE FROM " + table
    sql += " " + whereSql
    Exec(connection, sql)
# end DeleteWhere

######################################
# Load CSV
# Load table from a CSV file
# flag if it has a header
######################################
def LoadCSV(connection, table, fileNameIn, header=True) :
    with connection.cursor() as cur:    
        # load from CSV File 
        fileSize = os.path.getsize(fileNameIn)
        print("Loading table: " + table + " from: " + fileNameIn + " filesize: " + str(fileSize))
        with open(fileNameIn, 'r') as dbFile:
            sql = "COPY " + table
            sql += " FROM  STDIN " # have to read file into STDIN
            sql += " DELIMITER E" + SINGLE_QT + COMMA + SINGLE_QT # COMMA delimited
            sql += " CSV"
            if (header) :
                sql += " HEADER"  #  with header
            sql += SQL_END
            print(sql)
            # have to use copy_expert to handle header
            cur.copy_expert(sql, dbFile, fileSize)
        # end with dbFile
    # end with cursor
# end LoadCSV

######################################
# Load CSV With ID
# Load from a CSV file that has a header
# Table has a SERIAL ID column as first column
######################################
def LoadCSV_WithID(connection, table, fileNameIn, header=True) :
    with connection.cursor() as cur:    
        # load from CSV File WITH HEADER
        fileSize = os.path.getsize(fileNameIn)
        print("Loading table: " + table + " from: " + fileNameIn + " filesize: " + str(fileSize))
        with open(fileNameIn, 'r') as dbFile:
            #dbFile , <tabe name>, tab-Seperated
            columns = getColumnNames(table)
            columns.remove("id")
            # print(columns)
            columnNames = ','.join(columns)
            sql = f"copy {table}({columnNames}) " 
            sql += " FROM  STDIN " # have to read file into STDIN
            sql += " DELIMITER E" + SINGLE_QT + COMMA + SINGLE_QT # COMMA delimited
            sql += " CSV"
            if (header) :
                sql += " HEADER"  #  with header
            sql += SQL_END
            print(sql)
            cur.copy_expert(sql, dbFile, fileSize)
        # end with dbFile
    # end with cursor
# end LoadCSV_WithID

######################################
# Load TAB
# Load table from a TAB delimited file
# flag if it has a header
######################################
def LoadTAB(connection, table, fileNameIn, header=True) :
    with connection.cursor() as cur:    
        # load from TAB File 
        fileSize = os.path.getsize(fileNameIn)
        print("Loading table: " + table + " from: " + fileNameIn + " filesize: " + str(fileSize))
        with open(fileNameIn, 'r') as dbFile:
            sql = "COPY " + table
            sql += " FROM  STDIN " # have to read file into STDIN
            sql += " DELIMITER E" + SINGLE_QT + TAB + SINGLE_QT # TAB delimited
            sql += " CSV"
            if (header) :
                sql += " HEADER"  #  with header
            sql += SQL_END
            print(sql)
            # have to use copy_expert to handle header
            cur.copy_expert(sql, dbFile, fileSize)
        # end with dbFile
    # end with cursor
# end LoadTAB

#####################################################
# Get Column Names from a table
# This is used when loading a table with a serial ID
# to return the non-ID columns being loaded
#####################################################
def getColumnNames(table) :
    columnNames = []
    with Connect() as conn:
        with conn.cursor() as cur:
            # Select column names for table
            sql = "SELECT column_name from information_schema.columns where table_schema = 'public' and table_name='" + table + "'"
            cur.execute(sql)
            columnNames = [row[0] for row in cur]
        # end with cursor
    # end connection
    print("Column names: " + str(columnNames))
    return columnNames
# end getColumnNames

######################################
# SELECT Count(*)
# WHERE
# Return the count of rows selected
######################################
def SelectCountWhere(connection, table, whereSql="") :
    sql = "SELECT COUNT(*) FROM " + table
    sql += " " + whereSql
    with connection.cursor() as cursor:
        print(sql)
        cursor.execute(sql)
        recordCount = cursor.fetchone()
        print("FOUND " + str(recordCount[0]) + " ROWS in " + table)
    # end with cursor             
# end SelectCountWhere
