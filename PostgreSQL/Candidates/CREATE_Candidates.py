import psycopg2 

SINGLE_QT = "'"
###########################################
# Create Candidates table
# This holds the code and name used for state offices
# This is used for linking donations to a candidate
###########################################
# Candidates
#   id - integer primary key
#   year
#   office -> office.code
#   district - integer default NULL for state-wide races
#   lastname - varchar(30)
#   firatname - varchar(30)
#   party   - DEM or REP
#   status  - Defeated / Elected
#   primary - Won / Eliminated / Unopposed
#   general - Won / Eliminated / Unopposed
###########################################

with psycopg2.connect( host='localhost', user='postgres', password='postgres', dbname='postgres') as conn:

    sql = "DROP TABLE IF EXISTS candidates;"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
        print("DELETED TABLE")
    # end with cursor
    
    sql = "CREATE TABLE IF NOT EXISTS candidates"
    sql += " ( "
    sql += " id SERIAL PRIMARY KEY,"
    sql += " year integer NOT NULL,"
    sql += " office char(3) NOT NULL,"
    sql += " district integer,"
    sql += " lastname varchar(30),"
    sql += " firstname varchar(30),"
    sql += " party char(3) NOT NULL,"
    sql += " status varchar(10),"
    sql += " primary_result varchar(10),"  # primary is a keyword
    sql += " general_result varchar(10)"
    ## sql += "CONSTRAINT candidates_pkey  (id)"
    sql += " ); "
    
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
        print("CREATED TABLE")
    # end with cursor

# end with connection
print("****************************")
print("Finished")