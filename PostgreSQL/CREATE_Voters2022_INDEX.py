import psycopg2 

SINGLE_QT = "'"
###########################################
# Create Voter Table
# This holds the voter's data parsed from the voter files
# Street Address information is removed
###########################################

with psycopg2.connect( host='localhost', user='postgres', password='postgres', dbname='postgres') as conn:

    ##########################################################
    # Create Indexes
    ##########################################################
    sql = "DROP INDEX IF EXISTS voters_2022_gen_active_idx;"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
    # end with cursor
    sql = "CREATE INDEX IF NOT EXISTS voters_2022_gen_active_idx"
    sql += " ON voters_2022_gen USING btree"
    sql += " (active ASC NULLS LAST)"
    sql += ";"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
    # end with cursor

    sql = "DROP INDEX IF EXISTS voters_2022_gen_county_idx;"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
    # end with cursor
    sql = "CREATE INDEX IF NOT EXISTS voters_2022_gen_county_idx"
    sql += " ON voters_2022_gen USING btree"
    sql += " (county ASC NULLS LAST)"
    sql += ";"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
    # end with cursor

    sql = "DROP INDEX IF EXISTS voters_2022_gen_party_idx;"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
    # end with cursor
    sql = "CREATE INDEX IF NOT EXISTS voters_2022_gen_party_idx"
    sql += " ON voters_2022_gen USING btree"
    sql += " (party ASC NULLS LAST)"
    sql += ";"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
    # end with cursor

    sql = "DROP INDEX IF EXISTS voters_2022_gen_house_idx;"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
    # end with cursor
    sql = "CREATE INDEX IF NOT EXISTS voters_2022_gen_house_idx"
    sql += " ON voters_2022_gen USING btree"
    sql += " (house ASC NULLS LAST)"
    sql += ";"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
    # end with cursor

    sql = "DROP INDEX IF EXISTS voters_2022_gen_senate_idx;"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
    # end with cursor
    sql = "CREATE INDEX IF NOT EXISTS voters_2022_gen_senate_idx"
    sql += " ON voters_2022_gen USING btree"
    sql += " (senate ASC NULLS LAST)"
    sql += ";"
    with conn.cursor() as cur:
        print(sql)
        cur.execute(sql)
    # end with cursor
# end with connection
print("****************************")
print("Finished")