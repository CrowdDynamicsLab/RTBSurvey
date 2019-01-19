from random import shuffle, random

from selenium.common.exceptions import TimeoutException

from OpenWPM.automation import TaskManager, CommandSequence
import os, time
from urlparse import urlparse, urljoin
from OpenWPM.automation.Commands.utils.webdriver_extensions import scroll_down, \
    scroll_to_element, move_to_element, is_75percent_scrolled, scroll_percent

MAX_PAGES_PER_LANDING_PAGE = 10

class CrawlStrategy():
    # crawl_pages is just a list of urls to navigate to
    # landing and extraction is dictionary with keys corresponding to pages where more links can be visited
    # from according to the extraction rule in the value
    # so a key/value pair might be
    # https://www.reddit.com/r/worldnews/ -> a function that gives a page element for the browser to click on
    def __init__(self, profile_name, crawl_pages, landing_and_extraction):
        self.profile_name = profile_name
        self.crawl_pages = crawl_pages
        self.landing_and_extraction = landing_and_extraction
        if not os.path.exists('profiles/{}/'.format(self.profile_name)):
            os.makedirs('profiles/{}/'.format(self.profile_name))
        if not os.path.exists('crawl_data/{}/'.format(self.profile_name)):
            os.makedirs('crawl_data/{}/'.format(self.profile_name))


    # just return true for now, can use this for throttling and time of day logic
    def can_crawl(self):
        return True

    def my_custom_function(self, num_pages, landing_page, rule):
        def result(**kwargs):
            webdriver = kwargs['driver']
            already_visited = set([])
            for i in range(num_pages):
                candidate_divs = rule(webdriver)
                valid_divs = []
                for cd in candidate_divs:
                    if cd.get_attribute("href") not in already_visited:
                        valid_divs.append(cd)
                shuffle(valid_divs)
                if len(valid_divs) == 0:
                    print 'WARNING: Tried to access div index {} but there were only {} valid_divs'.format(i, len(valid_divs))
                else:
                    href = valid_divs[i].get_attribute("href")
                    scroll_to_element(webdriver, valid_divs[i])
                    time.sleep(1)
                    move_to_element(webdriver, valid_divs[i])

                    already_visited.add(href)
                    webdriver.get(href)
                    print 'loaded {}'.format(href)

                    num_scrolls = 0
                    current_scroll_percent = -1
                    while not is_75percent_scrolled(webdriver) and num_scrolls < 40:
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
            while not is_75percent_scrolled(webdriver) and num_scrolls < 40:
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
            my_function = self.my_custom_function(MAX_PAGES_PER_LANDING_PAGE, lp, rule)
            command_sequence.run_custom_function(my_function, (), timeout=2100)
            command_sequence.dump_profile_cookies(100)
            manager.execute_command_sequence(command_sequence, index='**')

        manager.close()





if __name__ == "__main__":
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
                    #print href
                    hrefs.add(href)
                    result.append(anchor)
        return result


    # let's do the news crawl
    crawl_dict = {
        'https://www.reddit.com/r/worldnews/': get_reddit_stories,
        'https://www.reddit.com/r/news': get_reddit_stories
    }
    cs = CrawlStrategy("news", ['https://www.vox.com'], crawl_dict)
    cs.crawl()

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
    cs = CrawlStrategy("substantive_news", fixed_crawls, crawl_dict)
    cs.crawl()

