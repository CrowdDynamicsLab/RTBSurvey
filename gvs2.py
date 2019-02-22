from extractors import get_wsj_links
from CrawlStrategy import CrawlStrategy

def setup_gvs2():
    crawl_strategies = []

    # let's do the news crawl
    crawl_dict = {
        'https://www.wsj.com/': get_wsj_links
    }

    cs = CrawlStrategy("wsj", [], crawl_dict) # using default time of day and interval restrictions
    crawl_strategies.append(cs)

    return crawl_strategies