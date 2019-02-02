from extractors import get_reddit_stories
from CrawlStrategy import CrawlStrategy

def setup_barber5_reddit():
    crawl_strategies = []

    # let's do the news crawl
    crawl_dict = {
        'https://www.reddit.com/r/worldnews/': get_reddit_stories,
        'https://www.reddit.com/r/news': get_reddit_stories
    }

    cs = CrawlStrategy("news", [], crawl_dict) # using default time of day and interval restrictions
    crawl_strategies.append(cs)

    # and the "substantive" news crawl
    crawl_dict = {
        "https://www.reddit.com/r/InDepthStories": get_reddit_stories,
        "https://www.reddit.com/r/geopolitics/": get_reddit_stories,
        "https://www.reddit.com/r/foreignpolicy/": get_reddit_stories
    }
    fixed_crawls = [
        'https://www.economist.com/',
        'https://www.foreignaffairs.com/',
        'https://monocle.com/'
    ]
    time_restrictions = {
        'crawl_interval': 780
    }
    cs = CrawlStrategy("substantive_news", fixed_crawls, crawl_dict, time_restrictions)
    crawl_strategies.append(cs)
    return crawl_strategies