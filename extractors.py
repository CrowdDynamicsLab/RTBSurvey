from urlparse import urlparse, urljoin


# The logic of CrawlSrategy.crawl() will visit a landing page, load it and then call the extractor function
# used to construct the CrawlStrategy object. It will call this function with a selenium webdriver as an argument
# any extractor function can use this webdriver to find elements of the DOM which contain links the crawler should
# visit.
# You must return a list of WebElements which have an 'href' attribute
# as the crawler will iterate through this list and construct a list of links to visit
# by asking each of the WebElements returned by this function for the attribute href
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
