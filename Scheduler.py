import time, datetime
from random import shuffle
import barber5
import nc7
import traceback

if __name__ == "__main__":
    crawl_strategies = []
    crawl_strategies.extend(barber5.setup_barber5_reddit())
    crawl_strategies.extend(nc7.setup_professional())
    crawl_strategies.extend(nc7.setup_cooking())
    crawl_strategies.extend(nc7.setup_ycomb())
    shuffle(crawl_strategies)

    while True:
        for cs in crawl_strategies:
        	try:
	            if cs.can_crawl():
	                print '{} strategy {} is allowed to crawl, doing so now'.format(datetime.datetime.now().isoformat(' '), cs.profile_name)
	                cs.crawl()            
	        except Exception as e:
	        	print("exception while trying to crawl")
	        	print(traceback.format_exc())
        time.sleep(60)
