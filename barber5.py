from extractors import get_reddit_wrapper
from CrawlStrategy import CrawlStrategy

def setup_barber5_reddit():
    crawl_strategies = []

    time_restrictions = {
        'crawl_interval': 720        
    }

    # let's do the news crawl
    crawl_dict = {
        'https://www.reddit.com/r/worldnews/': get_reddit_wrapper(),
        'https://www.reddit.com/r/news': get_reddit_wrapper()
    }

    cs = CrawlStrategy("news", [], crawl_dict, time_restrictions)
    crawl_strategies.append(cs)

    # and the "substantive" news crawl
    crawl_dict = {
        "https://www.reddit.com/r/InDepthStories": get_reddit_wrapper(),
        "https://www.reddit.com/r/geopolitics/": get_reddit_wrapper(),
        "https://www.reddit.com/r/foreignpolicy/": get_reddit_wrapper(3)
    }
    fixed_crawls = [
        'https://www.economist.com/',
        'https://www.foreignaffairs.com/',
        'https://monocle.com/'
    ]

    cs = CrawlStrategy("substantive_news", fixed_crawls, crawl_dict, time_restrictions)
    crawl_strategies.append(cs)

    crawl_dict = {
        'https://www.reddit.com/r/malefashionadvice/': get_reddit_wrapper(),
        'https://www.reddit.com/r/Sneakers/': get_reddit_wrapper(),
        'https://www.reddit.com/r/news': get_reddit_wrapper(5)
    }
    cs = CrawlStrategy("malefashion", [], crawl_dict, time_restrictions)
    crawl_strategies.append(cs)

    crawl_dict = {
        'https://www.reddit.com/r/TwoXChromosomes/': get_reddit_wrapper(),
        'https://www.reddit.com/r/news': get_reddit_wrapper(5)
    }

    cs = CrawlStrategy('twox', [], crawl_dict, time_restrictions)
    crawl_strategies.append(cs)

    crawl_dict = {
        'https://www.reddit.com/r/raisingKids': get_reddit_wrapper(),
        'https://www.reddit.com/r/Newparents': get_reddit_wrapper(),
        'https://www.reddit.com/r/news': get_reddit_wrapper(5)
    }
    cs = CrawlStrategy('parenting', [], crawl_dict, time_restrictions)
    crawl_strategies.append(cs)

    return crawl_strategies