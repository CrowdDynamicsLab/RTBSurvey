import sqlite3
from sqlite3 import Error
from auction import Bid, Auction
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



conn = create_connection('crawl_data/ycombinator/crawl-data.sqlite')
rows = select_all(conn)

rubicon_auctions = []

for row in rows:
    if "fastlane" in row[3]:
        print(len(row[14]))
        if len(row[14]) > 2000:
            rubicon_auctions.append(gen_auction(row,'rubicon'))

def gen_auction(auction_data, network_name):
    #still to do - only one bid per auction?

    XFPQggAAAAAaSi1bP4UDtgpE_ocUpJhyeECxSA
