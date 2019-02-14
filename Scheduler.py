import time, datetime
from random import shuffle
from barber5 import setup_barber5_reddit

from gvs2 import setup_gvs2



from nc7 import setup_nick_irl, setup_ycomb


if __name__ == "__main__":
    crawl_strategies = []
    crawl_strategies.extend(setup_ycomb())
    crawl_strategies.extend(setup_barber5_reddit())
    crawl_strategies.extend(setup_nick_irl())
    crawl_strategies.extend(setup_gvs2())
    shuffle(crawl_strategies)
    while True:
        for cs in crawl_strategies:
            if cs.can_crawl():
                print '{} strategy {} is allowed to crawl, doing so now'.format(datetime.datetime.now().isoformat(' '), cs.profile_name)
                cs.crawl()
        time.sleep(15*60)

