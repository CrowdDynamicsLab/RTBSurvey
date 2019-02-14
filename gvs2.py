from extractors import get_wsj_links,get_reddit_wrapper
from CrawlStrategy import CrawlStrategy

def setup_gvs2():
    crawl_strategies = []

    # WSJ crawl
    crawl_dict = {
        'https://www.wsj.com/': get_wsj_links
    }

    cs = CrawlStrategy("wsj", [], crawl_dict) # using default time of day and interval restrictions
    crawl_strategies.append(cs)

    crawl_dict = {
        'https://www.reddit.com/r/iphone/': get_reddit_wrapper(),
        'https://www.reddit.com/r/LaptopDeals/': get_reddit_wrapper(),
        'https://www.reddit.com/r/technology': get_reddit_wrapper()
    }
    cs = CrawlStrategy("techshopping", [], crawl_dict)  # using default time of day and interval restrictions
    crawl_strategies.append(cs)

    crawl_dict = {
        'https://www.reddit.com/r/sports/': get_reddit_wrapper(),
        'https://www.reddit.com/r/nba/': get_reddit_wrapper(),
        'https://www.reddit.com/r/fantasyfootball': get_reddit_wrapper()
    }
    cs = CrawlStrategy("sports", [], crawl_dict)  # using default time of day and interval restrictions
    crawl_strategies.append(cs)

    crawl_dict = {
        'https://www.reddit.com/r/worldnews/': get_reddit_wrapper(),
        'https://www.reddit.com/r/news': get_reddit_wrapper()
    }

    cs = CrawlStrategy("news", [], crawl_dict)  # using default time of day and interval restrictions
    crawl_strategies.append(cs)


    return crawl_strategies