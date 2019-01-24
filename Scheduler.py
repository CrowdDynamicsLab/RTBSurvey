from urlparse import urlparse, urljoin
import time, datetime
from CrawlStrategy import CrawlStrategy

def get_reddit_stories(webdriver):
    location = webdriver.current_url
    result = []
    hrefs = set([])
    anchors = webdriver.find_elements_by_tag_name('a')
    for anchor in anchors:
        href = anchor.get_attribute('href')
        if not href:
            continue
        href = urljoin(location, href)
        host = urlparse(href).hostname
        if host.find('reddit') == -1 and host.find('bit.ly') == -1:
            if href not in hrefs:
                # print href
                hrefs.add(href)
                result.append(anchor)
    return result

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
        'crawl_interval': 5,
        'time_of_day_min': '20:00:00',
        'time_of_day_max': '22:00:00'
    }
    cs = CrawlStrategy("substantive_news", fixed_crawls, crawl_dict, time_restrictions)
    crawl_strategies.append(cs)
    return crawl_strategies

if __name__ == "__main__":
    crawl_strategies = setup_barber5_reddit()
    while True:
        for cs in crawl_strategies:
            if cs.can_crawl():
                print '{} strategy {} is allowed to crawl, doing so now'.format(datetime.datetime.now().isoformat(' '), cs.profile_name)
                cs.crawl()
        time.sleep(10)
