from extractors import get_cfb, get_goldfish, get_ycomb_stories
from CrawlStrategy import CrawlStrategy

def setup_ycomb():
    crawl_strategies = []
    crawl_dict = {
        'https://news.ycombinator.com/': get_ycomb_stories
    }

    cs = CrawlStrategy('ycombinator', [], crawl_dict, time_restrictions)
    crawl_strategies.append(cs)
    return crawl_strategies

def setup_nick_irl():
    crawl_strategies = []
    crawl_dict = {
        'https://www.mtggoldfish.com/': get_goldfish,
        'https://www.channelfireball.com/': get_cfb
    }
    cs = CrawlStrategy('mtg', [], crawl_dict)
    crawl_strategies.append(cs)
    return crawl_strategies
