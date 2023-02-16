import psycopg2 

SINGLE_QT = "'"
###########################################
# Create INDEXES on Candidates table
###########################################

with psycopg2.connect( host='localhost', user='postgres', password='postgres', dbname='postgres') as conn:

    ##########################################################
    # Create Indexes
    ##########################################################
    sql = "DROP INDEX IF EXISTS candidates_year_idx;"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
    # end with cursor
    sql = "CREATE INDEX IF NOT EXISTS candidates_year_idx"
    sql += " ON candidates USING btree"
    sql += " (year ASC NULLS LAST)"
    sql += ";"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
    # end with cursor

    sql = "DROP INDEX IF EXISTS candidates_office_idx;"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
    # end with cursor
    sql = "CREATE INDEX IF NOT EXISTS candidates_office_idx"
    sql += " ON candidates USING btree"
    sql += " (office ASC NULLS LAST)"
    sql += ";"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
    # end with cursor

    sql = "DROP INDEX IF EXISTS candidates_party_idx;"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
    # end with cursor
    sql = "CREATE INDEX IF NOT EXISTS candidates_party_idx"
    sql += " ON candidates USING btree"
    sql += " (party ASC NULLS LAST)"
    sql += ";"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
    # end with cursor


# end with connection
print("****************************")
print("Finished")