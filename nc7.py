import extractors as ex
from CrawlStrategy import CrawlStrategy

def setup_ycomb():
    crawl_strategies = []
    crawl_dict = {
        'https://news.ycombinator.com/': ex.get_ycomb_stories
    }

    cs = CrawlStrategy('ycombinator', [], crawl_dict)
    crawl_strategies.append(cs)
    return crawl_strategies

def setup_nick_irl():
    crawl_strategies = []
    crawl_dict = {
        'https://www.mtggoldfish.com/': ex.get_goldfish,
        'https://www.channelfireball.com/': ex.get_cfb
    }
    cs = CrawlStrategy('mtg', [], crawl_dict)
    crawl_strategies.append(cs)
    return crawl_strategies

def setup_pop_sports():

    crawl_strategies = []

    crawl_dict = {
        "https://www.reddit.com/r/nfl/": ex.get_reddit_stories,
        "https://www.reddit.com/r/nba/": ex.get_reddit_stories,
        "https://www.reddit.com/r/baseball/": ex.get_reddit_stories,
        "https://www.reddit.com/r/hockey/": ex.get_reddit_stories,
        "https://www.reddit.com/r/soccer/": ex.get_reddit_stories
    }

    cs = CrawlStrategy('pop_sports', [], crawl_dict)
    crawl_strategies.append(cs)
    return crawl_strategies

def setup_niche_sports():

    crawl_strategies = []

    crawl_dict = {
        "https://www.reddit.com/r/Cricket/": ex.get_reddit_stories,
        "https://www.reddit.com/r/waterpolo/": ex.get_reddit_stories,
        "https://www.reddit.com/r/golf/": ex.get_reddit_stories
    }

    cs = CrawlStrategy('niche_sports', [], crawl_dict)
    crawl_strategies.append(cs)
    return crawl_strategies

def setup_liberal():

    crawl_strategies = []

    crawl_dict = {
        "https://www.vox.com/": ex.get_vox_articles,
        "https://slate.com/":ex.get_slate_articles,
        "https://www.huffingtonpost.com": ex.get_huff_articles,
        "https://www.reddit.com/r/TwoXChromosomes/": ex.get_reddit_stories
    }

    cs = CrawlStrategy('liberal', [], crawl_dict)
    crawl_strategies.append(cs)
    return crawl_strategies

def setup_conservative():

    crawl_strategies = []

    crawl_dict = {
        "https://www.breitbart.com": ex.get_ac_articles,
        "https://www.theamericanconservative.com": ex.get_ac_articles,
        "http://thefederalist.com": ex.get_ac_articles,
        "https://www.reddit.com/r/The_Donald/": ex.get_reddit_stories
    }

    fixed_crawls = [
        'https://vox.com',
        'https://www.economist.com/',
        'https://www.foreignaffairs.com/'
    ]

    cs = CrawlStrategy('conservative', fixed_crawls, crawl_dict, {'crawl_interval':1})
    crawl_strategies.append(cs)
    return crawl_strategies

def setup_professional():

    crawl_strategies = []

    crawl_dict = {
        "https://www.bloomberg.com": ex.get_bloomberg_articles,
        "https://www.economist.com": ex.get_economist_articles,
        "https://www.wsj.com": ex.get_wsj_artcles
    }

    cs = CrawlStrategy('neutral', [], crawl_dict)
    crawl_strategies.append(cs)
    return crawl_strategies

def setup_cooking():

    crawl_strategies = []

    crawl_dict = {
        "https://www.cooking.nytimes.com": ex.get_cookingnyt,
        "https://www.reddit.com/r/recipes": ex.get_reddit_stories,
        "https://www.allrecipes.com/": ex.get_allrec
    }
