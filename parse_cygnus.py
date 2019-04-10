import sqlite3
from sqlite3 import Error
import auction
import re
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print e
    return None


def select_all(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM http_responses")
    return cur.fetchall()

crawl_data_dir = 'crawl_data/voxonly/crawl-data.sqlite'

conn = create_connection(crawl_data_dir)
rows = select_all(conn)

auctions_list = []

for row in rows:
    if "cygnus" in row[3]:
        response = row[14].replace('\\', '/')
        #print(response)
        auctions_list.append(auction.parse_response(row=row, response = response,price_var = '/"price/"', cid_var = '/"cid/"' , dim_vars = ['/"w/"','/"h/"'], adname_var = '/"advbrand/"', adid_var = '/"advbrandid/"', val_offset = 1, str_offset=3))

        #each var argument is a unique identifier for the value you're looking for - make sure there is no conflict or this will mess up
        #val_offset is number of characters to skip after identifier for numeric values; in the case of cygnus, there's a ':' character so offset =1
        #str_offset is number of characters to skip for non-numeric values; in the case of cygnus, there's ':/"' so I set it to 3.

for a in auctions_list:
    print(a)
