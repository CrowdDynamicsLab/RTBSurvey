from urlparse import urlparse, urljoin
import time
from random import shuffle
from OpenWPM.automation.Commands.utils.webdriver_extensions import scroll_to_bottom


# The logic of CrawlSrategy.crawl() will visit a landing page, load it and then call the extractor function
# used to construct the CrawlStrategy object. It will call this function with a selenium webdriver as an argument
# any extractor function can use this webdriver to find elements of the DOM which contain links the crawler should
# visit.
# You must return a list of WebElements which have an 'href' attribute
# as the crawler will iterate through this list and construct a list of links to visit
# by asking each of the WebElements returned by this function for the attribute href



def get_ycomb_stories(webdriver):
    location = webdriver.current_url
    result = []
    hrefs = set([])
    anchors = webdriver.find_elements_by_class_name('storylink')
    for anchor in anchors[1:3]:
        href = anchor.get_attribute('href')
        if not href:
            continue
        hrefs.add(href)
        #print(href)
        result.append(anchor)

    return result

def get_goldfish(webdriver):
    location = webdriver.current_url
    result = []
    hrefs = set([])
    anchors = webdriver.find_elements_by_tag_name('a')
    for anchor in anchors:
        href = anchor.get_attribute('href')
        if not href:
            continue
        href = urljoin(location, href)
        if 'article' not in href:
            continue
        host = urlparse(href).hostname
        if href not in hrefs:
            hrefs.add(href)
            result.append(anchor)
    print(hrefs)
    return result

def get_cfb(webdriver):
    location = webdriver.current_url
    result = []
    hrefs = set([])
    anchors = webdriver.find_elements_by_tag_name('a')
    for anchor in anchors:
        href = anchor.get_attribute('href')
        if not href:
            continue
        href = urljoin(location, href)
        if 'article' not in href:
            continue
        host = urlparse(href).hostname
        if href not in hrefs:
            hrefs.add(href)
            result.append(anchor)
    print(hrefs)
    return result

def get_reddit_wrapper(max_hrefs=10):
    def get_reddit_stories(webdriver):
        location = webdriver.current_url
        scroll_to_bottom(webdriver)
        time.sleep(3)
        scroll_to_bottom(webdriver)
        time.sleep(3)
        result = []
        hrefs = set([])
        anchors = webdriver.find_elements_by_tag_name('a')
        for anchor in anchors:
            href = anchor.get_attribute('href')
            if not href:
                continue
            href = urljoin(location, href)
            host = urlparse(href).hostname
            if host.find('reddit') == -1 and host.find('bit.ly') == -1 and host.find('redd.it') == -1 and host.find('imgur') == -1:
                if href not in hrefs:
                    # print href
                    hrefs.add(href)
                    result.append(anchor)

        if len(result) > max_hrefs:
            shuffle(result)
            result = result[:max_hrefs]
        return result
    return get_reddit_stories

