import sqlite3
from sqlite3 import Error
import auction
import re
import numpy as np
import matplotlib.pyplot as plt
import time

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

crawl_data_dir = 'crawl_data/liberal/crawl-data.sqlite'

conn = create_connection(crawl_data_dir)



cur = conn.cursor()
cur.execute("SELECT response_content, time_stamp, referrer FROM http_responses WHERE url like '%cygnus%' AND referrer =?",("https://www.vox.com/",))
result = cur.fetchall()
#print(result)
auctions_list = []

for row in result:
    response = row[0].replace('\\','/')
    auctions_list.append(auction.parse_response(row=row, response = response,price_var = '/"price/"', cid_var = '/"cid/"' , dim_vars = ['/"w/"','/"h/"'], adname_var = '/"advbrand/"', adid_var = '/"advbrandid/"', val_offset = 1, str_offset=3))


auctions_list=  sorted(auctions_list)

new_auctions=[]

lower=0
for i in range(1,len(auctions_list)):
    if time.mktime(auctions_list[i].datetime)-time.mktime(auctions_list[i-1].datetime) >2000:
        new_auctions.append(auction.merge_auctions(auctions_list[lower:i]))
        lower = i

new_auctions.append(auction.merge_auctions(auctions_list[lower:(len(auctions_list)+1)]))

avg_bids = []
num_bids = []
bid_sd = []
winning_bids =[]
times =[]


for auction in auctions_list:
    bid_sum = 0
    sd_temp = []
    if len(auction.bids)==0:
        continue
    for bid in auction.bids:
        bid_sum+=bid.price
        sd_temp.append(bid.price)
    avg_bids.append(bid_sum/len(sd_temp))
    num_bids.append(len(sd_temp))
    bid_sd.append(np.std(sd_temp))
    winning_bids.append(auction.get_winning_bid().price)
    times.append(time.mktime(auction.datetime))


diffs=[]
for i in range(len(times)-1):
    diffs.append(times[i+1]-times[i])



x = range(len(avg_bids))
plt.scatter(x, avg_bids)
plt.show()

plt.scatter(x, num_bids)
plt.show()

plt.scatter(x,winning_bids)
plt.show()

plt.scatter(x,times)
plt.show()

x = range(len(diffs))
plt.scatter(x,diffs)
plt.show()


avg_bids = []
num_bids = []
bid_sd = []
winning_bids =[]
times =[]


for auction in new_auctions:
    bid_sum = 0
    sd_temp = []
    if len(auction.bids)==0:
        continue
    for bid in auction.bids:
        bid_sum+=bid.price
        sd_temp.append(bid.price)
    avg_bids.append(bid_sum/len(sd_temp))
    num_bids.append(len(sd_temp))
    bid_sd.append(np.std(sd_temp))
    winning_bids.append(auction.get_winning_bid().price)
    times.append(time.mktime(auction.datetime))


diffs=[]
for i in range(len(times)-1):
    diffs.append(times[i+1]-times[i])

x = range(len(diffs))
plt.scatter(x,diffs)
plt.show()

x = range(len(avg_bids))
plt.scatter(x,times)
plt.show()
plt.scatter(x, avg_bids)
plt.show()

plt.scatter(x, num_bids)
plt.show()

plt.scatter(x,winning_bids)
plt.show()




'''
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
'''
