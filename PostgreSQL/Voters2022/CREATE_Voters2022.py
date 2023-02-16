import psycopg2 

SINGLE_QT = "'"
###########################################
# Create Voter Table
# This holds the voter's data parsed from the voter files
# Street Address information is removed
###########################################

with psycopg2.connect( host='localhost', user='postgres', password='postgres', dbname='postgres') as conn:

    sql = "DROP TABLE IF EXISTS voters_2022_gen;"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
        print("DELETED TABLE")
    # end with cursor
    
    sql = "CREATE TABLE IF NOT EXISTS voters_2022_gen"
    sql += " ( "
    sql += " county character varying(3) NOT NULL,"
    sql += " voterid integer NOT NULL,"
    sql += " lastname character varying(30),"
    sql += " suffix character varying(5),"
    sql += " firstname character varying(30),"
    sql += " middle character varying(30),"
    sql += " exempt character(1) NOT NULL,"
    sql += " rescity character varying(40),"
    sql += " resstate character(2),"
    sql += " reszip character varying(10) ,"
    sql += " gender character(1),"
    sql += " race integer,"
    sql += " birth_date date,"
    sql += " registration_date date,"
    sql += " party character varying(3) NOT NULL,"
    sql += " precinct character varying(6) NOT NULL,"
    sql += " active character varying(3) NOT NULL,"
    sql += " congress integer,"
    sql += " house integer,"
    sql += " senate integer,"
    sql += " countycom integer,"
    sql += " schoolboard integer,"
    sql += "CONSTRAINT voters_2022_gen_pkey PRIMARY KEY (voterid)"
    sql += " ); "
    
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
        print("CREATED TABLE")
    # end with cursor

# end with connection
print("****************************")
print("Finished")