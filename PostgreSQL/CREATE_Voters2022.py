import os
import shutil
import psycopg2 
import csv
from csv import DictReader

SQT = "'"

dirData = "F:\Voter Disks\Voter History"
dirVoterFiles = os.path.join(dirData, "Latest_2022", "DBFiles")

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
    sql += " firstname character varying(30),"
    sql += " middle character varying(30),"
    sql += " suffix character varying(5),"
    sql += " rescity character varying(40),"
    sql += " resstate character(2),"
    sql += " reszip character varying(10) ,"
    sql += " birth_date date,"
    sql += " party character varying(3) NOT NULL,"
    sql += " active character varying(3) NOT NULL,"
    sql += " gender character(1),"
    sql += " race character varying(20),"
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