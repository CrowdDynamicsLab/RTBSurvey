import traceback
from random import shuffle, random
import datetime
from OpenWPM.automation import TaskManager, CommandSequence
import os, time
from OpenWPM.automation.Commands.utils.webdriver_extensions import scroll_down, \
    is_60percent_scrolled, scroll_percent
from extractors import get_reddit_wrapper
import sqlite3

CRAWL_DATA_PATH = 'crawl_data'

class CrawlStrategy():
    # crawl_pages is just a list of urls to navigate to
    # landing and extraction is dictionary with keys corresponding to pages where more links can be visited
    # from according to the extraction rule in the value
    # so a key/value pair might be
    # https://www.reddit.com/r/worldnews/ -> a function that gives a page element for the browser to click on
    def __init__(self, profile_name, crawl_pages, landing_and_extraction, time_restrictions=None):
        self.profile_name = profile_name
        self.crawl_pages = crawl_pages
        self.landing_and_extraction = landing_and_extraction
        if not os.path.exists('profiles/{}/'.format(self.profile_name)):
            os.makedirs('profiles/{}/'.format(self.profile_name))
        if not os.path.exists('crawl_data/{}/'.format(self.profile_name)):
            os.makedirs('crawl_data/{}/'.format(self.profile_name))
        if not time_restrictions:
            time_restrictions = {}

        if 'time_of_day_min' not in time_restrictions:
            self.time_of_day_min = "00:00:01"
        else:
            self.time_of_day_min = time_restrictions['time_of_day_min']
        if 'time_of_day_max' not in time_restrictions:
            self.time_of_day_max = "23:59:59"
        else:
            self.time_of_day_max = time_restrictions['time_of_day_max']
        if 'crawl_interval' not in time_restrictions:
            self.crawl_interval = 720  # default to crawl no more often than every 12 hours
        else:
            self.crawl_interval = time_restrictions['crawl_interval']
        self.last_crawl = datetime.datetime(2000, 12, 1)


    # just return true for now, can use this for throttling and time of day logic
    def can_crawl(self):
        if datetime.datetime.now() < self.last_crawl + datetime.timedelta(minutes=self.crawl_interval):
            return False
        now = datetime.datetime.now()
        min_array = self.time_of_day_min.split(':')
        min_dt = datetime.datetime(now.year, now.month, now.day, hour=int(min_array[0]), minute=int(min_array[1]), second=int(min_array[2]))
        if now < min_dt:
            return False
        max_array = self.time_of_day_max.split(':')
        max_dt = datetime.datetime(now.year, now.month, now.day, hour=int(max_array[0]), minute=int(max_array[1]), second=int(max_array[2]))
        if now > max_dt:
            return False
        return True


    def my_custom_function(self, landing_page, rule):
        def result(**kwargs):

            webdriver = kwargs['driver']
            already_visited = set([])
            candidate_divs = rule(webdriver)
            valid_divs = []
            for cd in candidate_divs:
                if cd.get_attribute("href") not in already_visited:
                    try:
                        db_connection = sqlite3.connect('{}/{}/crawl-data.sqlite'.format(CRAWL_DATA_PATH, self.profile_name))
                        db_cursor = db_connection.cursor()
                        db_cursor.execute("SELECT url from http_requests where url='%s'" % cd.get_attribute('href'))
                        results = db_cursor.fetchall()
                        print 'length of results for {} is {}'.format(cd.get_attribute('href'), len(results))
                        if len(results) == 0:
                            valid_divs.append(cd.get_attribute('href'))
                        db_connection.close()
                    except Exception as e:
                        print "database likely doesn't exist yet"
                        print traceback.format_exc()
            print 'got {} potential links'.format(len(valid_divs))
            shuffle(valid_divs)
            for href in valid_divs:
                webdriver.get(href)
                print 'loaded {}'.format(href)

                num_scrolls = 0
                current_scroll_percent = -1
                while not is_60percent_scrolled(webdriver) and num_scrolls < 40:
                    scroll_down(webdriver)
                    last_scroll_percent = current_scroll_percent
                    current_scroll_percent = scroll_percent(webdriver)
                    print 'last_percent: {}, current_percent: {}'.format(last_scroll_percent, current_scroll_percent)
                    if current_scroll_percent <= last_scroll_percent:
                        break
                    num_scrolls += 1
                    print 'num_scrolls: {}'.format(num_scrolls)
                    time.sleep(2*random())
                print 'done scrolling'
                webdriver.get(landing_page)
                time.sleep(3)
        return result


    def fixed_custom_function(self):
        def result(**kwargs):
            webdriver = kwargs['driver']
            num_scrolls = 0
            current_scroll_percent = -1
            while not is_60percent_scrolled(webdriver) and num_scrolls < 40:
                scroll_down(webdriver)
                last_scroll_percent = current_scroll_percent
                current_scroll_percent = scroll_percent(webdriver)
                print 'last_percent: {}, current_percent: {}'.format(last_scroll_percent, current_scroll_percent)
                if current_scroll_percent <= last_scroll_percent:
                    break
                num_scrolls += 1
                print 'num_scrolls: {}'.format(num_scrolls)
                time.sleep(2 * random())
            print 'done scrolling'
        return result

    def crawl(self):
        self.last_crawl = datetime.datetime.now()
        # initialize crawler
        manager_params, browser_params = TaskManager.load_default_params()
        browser_params[0]['http_instrument'] = True
        browser_params[0]['cookie_instrument'] = True
        browser_params[0]['save_json'] = True
        # ensures profile is saved
        browser_params[0]['profile_archive_dir'] = 'profiles/{}/'.format(self.profile_name)
        # logging
        manager_params['data_directory'] = 'crawl_data/{}/'.format(self.profile_name)
        manager_params['log_directory'] = 'crawl_data/{}/'.format(self.profile_name)
        # load profile if need be
        if os.path.isfile('profiles/{}/profile.tar'.format(self.profile_name)) or os.path.isfile('profiles/{}/profile.tar.gz'.format(self.profile_name)):
            browser_params[0]['profile_tar'] = 'profiles/{}/'.format(self.profile_name)
        manager = TaskManager.TaskManager(manager_params, browser_params)

        # crawl our fixed pages
        shuffle(self.crawl_pages)
        for site in self.crawl_pages:
            command_sequence = CommandSequence.CommandSequence(site)
            command_sequence.get(sleep=3, timeout=100)
            fixed_custom_function = self.fixed_custom_function()
            command_sequence.run_custom_function(fixed_custom_function, (), timeout=300)
            command_sequence.dump_profile_cookies(100)
            manager.execute_command_sequence(command_sequence, index='**')

        # crawl our landing pages plus their children
        for lp, rule in self.landing_and_extraction.iteritems():
            command_sequence = CommandSequence.CommandSequence(lp)
            command_sequence.get(sleep=3, timeout=100)
            my_function = self.my_custom_function(lp, rule)
            command_sequence.run_custom_function(my_function, (), timeout=2100)
            command_sequence.dump_profile_cookies(100)
            manager.execute_command_sequence(command_sequence, index='**')

        manager.close()


if __name__ == "__main__":
    # let's do the news crawl
    crawl_dict = {
        'https://www.reddit.com/r/worldnews/': get_reddit_wrapper(),
        'https://www.reddit.com/r/news': get_reddit_wrapper()
    }
    cs = CrawlStrategy("news", [], crawl_dict)
    cs.crawl()

    # and the "substantive" news crawl
    crawl_dict = {
        "https://www.reddit.com/r/InDepthStories": get_reddit_wrapper(5),
        "https://www.reddit.com/r/geopolitics/": get_reddit_wrapper(5),
        "https://www.reddit.com/r/foreignpolicy/": get_reddit_wrapper(3)
    }
    fixed_crawls = [
        'https://www.economist.com/',
        'https://www.foreignaffairs.com/',
        'https://monocle.com/'
    ]
    cs = CrawlStrategy("substantive_news", fixed_crawls, crawl_dict)
    cs.crawl()
