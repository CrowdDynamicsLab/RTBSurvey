import time, datetime
from barber5 import setup_barber5_reddit
from gvs2 import setup_gvs2



if __name__ == "__main__":
    crawl_strategies = setup_gvs2()
    while True:
        for cs in crawl_strategies:
            if cs.can_crawl():
                print '{} strategy {} is allowed to crawl, doing so now'.format(datetime.datetime.now().isoformat(' '), cs.profile_name)
                cs.crawl()
        time.sleep(15*60)

