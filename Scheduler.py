import time, datetime
from barber5 import setup_barber5_reddit
import nc7

if __name__ == "__main__":
    crawl_strategies = nc7.setup_liberal()
    while True:
        for cs in crawl_strategies:
            if cs.can_crawl():
                print '{} strategy {} is allowed to crawl, doing so now'.format(datetime.datetime.now().isoformat(' '), cs.profile_name)
                cs.crawl()
        time.sleep(15*60)
