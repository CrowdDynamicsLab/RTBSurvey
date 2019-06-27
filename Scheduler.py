import time, datetime
from random import shuffle
import barber5

if __name__ == "__main__":
    crawl_strategies = []
    crawl_strategies.extend(barber5.setup_barber5_reddit())
    shuffle(crawl_strategies)

    while True:
        for cs in crawl_strategies:
            if cs.can_crawl():
                print '{} strategy {} is allowed to crawl, doing so now'.format(datetime.datetime.now().isoformat(' '), cs.profile_name)
                cs.crawl()            
        time.sleep(60)
