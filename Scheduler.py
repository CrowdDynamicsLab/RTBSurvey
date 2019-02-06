import time, datetime
from barber5 import setup_barber5_reddit



if __name__ == "__main__":
    crawl_strategies = setup_barber5_reddit()
    while True:
        for cs in crawl_strategies:
            if cs.can_crawl():
                print '{} strategy {} is allowed to crawl, doing so now'.format(datetime.datetime.now().isoformat(' '), cs.profile_name)
                cs.crawl()
        time.sleep(15*60)
