import time, datetime
from random import shuffle
from barber5 import setup_barber5_reddit
import nc7

if __name__ == "__main__":
    crawl_strategies = nc7.setup_liberal()


from gvs2 import setup_gvs2



from nc7 import setup_nick_irl, setup_ycomb


if __name__ == "__main__":
    crawl_strategies = []
    crawl_strategies.extend(nc7.setup_conservative())
    shuffle(crawl_strategies)

    while True:
        for cs in crawl_strategies:
            if cs.can_crawl():
                print '{} strategy {} is allowed to crawl, doing so now'.format(datetime.datetime.now().isoformat(' '), cs.profile_name)
                cs.crawl()
        time.sleep(60)
