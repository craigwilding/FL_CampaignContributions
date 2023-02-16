import psycopg2 

SINGLE_QT = "'"
###########################################
# Create Offices table
# This holds the code and name used for state offices
# Offices
#   code - char(3)
#   name - varchar(30)
###########################################

with psycopg2.connect( host='localhost', user='postgres', password='postgres', dbname='postgres') as conn:

    sql = "DROP TABLE IF EXISTS offices;"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
        print("DELETED TABLE")
    # end with cursor
    
    sql = "CREATE TABLE IF NOT EXISTS offices"
    sql += " ( "
    sql += " code char(3) NOT NULL,"
    sql += " name character varying(30) NOT NULL,"
    sql += "CONSTRAINT offices_pkey PRIMARY KEY (code)"
    sql += " ); "
    
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
        print("CREATED TABLE")
    # end with cursor

# end with connection
print("****************************")
print("Finished")