import psycopg2


with psycopg2.connect( host='localhost', user='postgres', password='postgres', dbname='postgres') as conn:
    with conn.cursor() as cur:
        sql = "SELECT county, COUNT(voterid) FROM voters_2022_gen"
        sql += " GROUP BY county"
        sql += " ORDER BY county"
        print(sql)
        cur.execute(sql)
        recordCounts = cur.fetchall()
        for record in recordCounts :
            print(str(record))
        # end for recordCounts
    # end with cursor
# end with connection