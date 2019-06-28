import traceback
from random import shuffle, random
import datetime
from OpenWPM.automation import TaskManager, CommandSequence
import os
import time
from OpenWPM.automation.Commands.utils.webdriver_extensions import scroll_down, \
    is_percent_scrolled, scroll_percent
from extractors import get_reddit_wrapper
from OpenWPM.automation.SocketInterface import clientsocket
from OpenWPM.automation.utilities import db_utils

CRAWL_DATA_PATH = 'crawl_data'

IGNORE_URLS = ['imgur.com', 'youtu.be', 'youtube.com', 'giphy.com', 'twitter.com', 't.co/', 'reddit.com', 'bit.ly',
               'redd.it', 'instagram.com', 'overcast.fm/']

BASELINE_PAGES = ['http://ww.vox.com', 'http://www.townhall.com', 'http://www.nypost.com', 'http://www.nytimes.com', 'http://www.wired.com', 'http://www.arstechnica.com']


class CrawlStrategy:
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
        min_dt = datetime.datetime(now.year, now.month, now.day, hour=int(min_array[0]), minute=int(min_array[1]),
                                   second=int(min_array[2]))
        if now < min_dt:
            return False
        max_array = self.time_of_day_max.split(':')
        max_dt = datetime.datetime(now.year, now.month, now.day, hour=int(max_array[0]), minute=int(max_array[1]),
                                   second=int(max_array[2]))
        if now > max_dt:
            return False
        return True

    @staticmethod
    def setup_visitdb(manager_params):
        # following the create pattern in
        # https://github.com/CrowdDynamicsLab/OpenWPM/blob/f731e6c35be0e0931941e2791cb003f7e09ec2fe/test/test_custom_function_command.py#L44
        # see
        # https://github.com/CrowdDynamicsLab/OpenWPM/blob/f731e6c35be0e0931941e2791cb003f7e09ec2fe/automation/DataAggregator/LocalAggregator.py#L92
        # for implementation of this part of sock.send() parsing
        sock = clientsocket()
        sock.connect(*manager_params['aggregator_address'])
        query = "CREATE TABLE IF NOT EXISTS crawl_visits (visit_id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                "crawl_id INTEGER NOT NULL, url TEXT NOT NULL)"
        sock.send(("create_table", query))
        sock.close()
        time.sleep(3)

    @staticmethod
    def insert_visit(manager_params, crawl_id, url):
        # following the insert pattern in
        # https://github.com/CrowdDynamicsLab/OpenWPM/blob/f731e6c35be0e0931941e2791cb003f7e09ec2fe/test/test_custom_function_command.py#L52
        # see
        # https://github.com/CrowdDynamicsLab/OpenWPM/blob/f731e6c35be0e0931941e2791cb003f7e09ec2fe/automation/DataAggregator/LocalAggregator.py#L99
        # for implementation of this part of sock.send() parsing
        sock = clientsocket()
        sock.connect(*manager_params['aggregator_address'])
        query = ('crawl_visits', {
            "crawl_id": crawl_id,
            "url": url
        })
        sock.send(query)
        sock.close()

    @staticmethod
    def query_visits(manager_params, href):
        for bad in IGNORE_URLS:
            if href.find(bad) != -1:
                return False
        query = "SELECT url FROM crawl_visits WHERE url='%s'" % href
        query_result = db_utils.query_db(
            manager_params['database_name'],
            query,
            as_tuple=True
        )
        return len(query_result) == 0

    def my_custom_function(self, landing_page, rule):
        def result(**kwargs):
            webdriver = kwargs['driver']
            manager_params = kwargs['manager_params']
            crawl_id = kwargs['browser_params']['crawl_id']
            self.setup_visitdb(manager_params)
            candidate_divs = rule(webdriver)
            valid_divs = []
            for cd in candidate_divs:
                href = cd.get_attribute('href')
                try:
                    if self.query_visits(manager_params, href):
                        print 'can crawl: {}'.format(href)
                        valid_divs.append(href)
                    else:
                        print 'cannot crawl (already visited or on blacklist): {}'.format(href)

                except Exception as e:
                    print "database likely doesn't exist yet"
                    print traceback.format_exc()
            print 'got {} potential links'.format(len(valid_divs))
            shuffle(valid_divs)
            for href in valid_divs:
                self.insert_visit(manager_params, crawl_id, href)
                webdriver.get(href)
                print 'loaded {}'.format(href)
                num_scrolls = 0
                current_scroll_percent = -1
                while not is_percent_scrolled(webdriver, .6) and num_scrolls < 40:
                    scroll_down(webdriver)
                    last_scroll_percent = current_scroll_percent
                    current_scroll_percent = scroll_percent(webdriver)
                    print 'last_percent: {}, current_percent: {}'.format(last_scroll_percent, current_scroll_percent)
                    if current_scroll_percent <= last_scroll_percent:
                        break
                    num_scrolls += 1
                    print 'num_scrolls: {}'.format(num_scrolls)
                    time.sleep(2*random())

                time.sleep(2 * random())
                print 'done scrolling'
                try:
                    webdriver.get(landing_page)
                except Exception as e:
                    print 'error getting {}'.format(landing_page)
                    print traceback.format_exc()

                time.sleep(3)
        return result

    @staticmethod
    def fixed_custom_function():
        def result(**kwargs):
            webdriver = kwargs['driver']
            num_scrolls = 0
            current_scroll_percent = -1
            while not is_percent_scrolled(webdriver, .6) and num_scrolls < 40:
                scroll_down(webdriver)
                last_scroll_percent = current_scroll_percent
                current_scroll_percent = scroll_percent(webdriver)
                print 'last_percent: {}, current_percent: {}'.format(last_scroll_percent, current_scroll_percent)
                if current_scroll_percent <= last_scroll_percent:
                    break
                num_scrolls += 1
                print 'num_scrolls: {}'.format(num_scrolls)
                time.sleep(2 * random())

            time.sleep(2 * random())
            print 'done scrolling'
        return result

    def crawl(self):
        self.last_crawl = datetime.datetime.now()
        # initialize crawler
        manager_params, browser_params = TaskManager.load_default_params()
        browser_params[0]['http_instrument'] = True
        browser_params[0]['save_all_content'] = True
        # ensures profile is saved
        browser_params[0]['headless']=True
        dump_folder = 'profiles/{}/'.format(self.profile_name)
        browser_params[0]['profile_archive_dir'] = dump_folder
        # logging
        manager_params['data_directory'] = 'crawl_data/{}/'.format(self.profile_name)
        manager_params['log_directory'] = 'crawl_data/{}/'.format(self.profile_name)
        # load profile if need be
        if os.path.isfile('profiles/{}/profile.tar'.format(self.profile_name)) or os.path.isfile(
                'profiles/{}/profile.tar.gz'.format(self.profile_name)):
            browser_params[0]['profile_tar'] = dump_folder
        manager = TaskManager.TaskManager(manager_params, browser_params)

        # crawl our fixed pages
        shuffle(self.crawl_pages)
        for site in self.crawl_pages:
            command_sequence = CommandSequence.CommandSequence(site)
            command_sequence.get(sleep=3, timeout=30)
            fixed_custom_function = self.fixed_custom_function()
            command_sequence.run_custom_function(fixed_custom_function, (), timeout=60)
            command_sequence.dump_profile(dump_folder)
            manager.execute_command_sequence(command_sequence, index='**')

        # crawl our landing pages plus their children
        for lp, rule in self.landing_and_extraction.iteritems():
            command_sequence = CommandSequence.CommandSequence(lp)
            command_sequence.get(sleep=3, timeout=100)
            my_function = self.my_custom_function(lp, rule)
            command_sequence.run_custom_function(my_function, (), timeout=3000)
            command_sequence.dump_profile(dump_folder)
            manager.execute_command_sequence(command_sequence, index='**')

        for site in BASELINE_PAGES:
            command_sequence = CommandSequence.CommandSequence(site)
            command_sequence.get(sleep=3, timeout=100)
            fixed_custom_function = self.fixed_custom_function()
            command_sequence.run_custom_function(fixed_custom_function, (), timeout=60)
            command_sequence.dump_profile(dump_folder)
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
