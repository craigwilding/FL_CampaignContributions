import psycopg2 
import sys
sys.path.insert(0, '/workspaces/vscode-remote-try-python/PostgreSQL')
import SQLCommands as SQL

SINGLE_QT = "'"
###########################################
# Create Contributions table
# This holds the contributions made to each candidate
###########################################
# cand_id,cand_lastname,cand_firstname,date,amount,contrib_type,contributor,
# occupation,inkind_desc,city,state,zipcode,donortype,donorindex
# Contributions
#   id - integer primary key
#   cand_id - candidate id (candidates)
#   cand_lastname - 
#   cand_firstname
#   date    - date contributed
#   amount
#   contrib_type - CHE, CAS, INK, LOA
#   contributor
#   occupation
#   inkind_desc
#   city
#   state
#   zipcode
#   donortype
#   donor_id
###########################################

with psycopg2.connect( host='localhost', user='postgres', password='postgres', dbname='postgres') as conn:

    sql = "DROP TABLE IF EXISTS contributions;"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
        print("DELETED TABLE")
    # end with cursor
    
    sql = "CREATE TABLE IF NOT EXISTS contributions"
    sql += " ( "
    sql += " id SERIAL PRIMARY KEY,"
    sql += " cand_id integer references candidates(id),"
    sql += " cand_lastname varchar(30),"
    sql += " cand_firstname varchar(30),"
    sql += " date DATE NOT NULL,"
    sql += " amount NUMERIC (10,2) NOT NULL,"
    sql += " contrib_type char(5),"
    sql += " contributor varchar(120),"
    sql += " occupation varchar(80),"
    sql += " inkind_desc varchar(80),"
    sql += " city varchar(30),"
    sql += " state char(5),"
    sql += " zipcode integer,"
    sql += " donortype char(5),"
    sql += " donor_id integer"
    sql += " ); "
    
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
        print("CREATED TABLE")
    # end with cursor

# end with connection

with SQL.Connect() as conn:

    ##########################################################
    # Create Indexes
    ##########################################################
    table = "contributions"
    SQL.DropIndex(conn, table, "cand_id")
    SQL.CreateIndex(conn, table, "cand_id")

    SQL.DropIndex(conn, table, "contributor")
    SQL.CreateIndex(conn, table, "contributor")

    SQL.DropIndex(conn, table, "zipcode")
    SQL.CreateIndex(conn, table, "zipcode")

    SQL.DropIndex(conn, table, "donortype")
    SQL.CreateIndex(conn, table, "donortype")
# end with connection - triggers commit
print("****************************")
print("Finished")
print("****************************")
print("Finished")