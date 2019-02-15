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
        if host.find('reddit') == -1 and host.find('bit.ly') == -1 and host.find('twitter') == -1:
            if href not in hrefs:
                # print href
                hrefs.add(href)
                result.append(anchor)
    print(hrefs)
    return result

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
    try:
        return result[0:3]
    except:
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
    try:
        return result[0:3]
    except:
        return result

def get_vox_articles(webdriver):
    location = webdriver.current_url
    result = []
    hrefs = set([])
    anchors = webdriver.find_elements_by_class_name('c-entry-box--compact__image-wrapper')
    for anchor in anchors:
        href = anchor.get_attribute('href')
        if not href:
            continue
        host = urlparse(href).hostname
        if href not in hrefs:
            hrefs.add(href)
            result.append(anchor)
    print(hrefs)
    try:
        return result[0:3]
    except:
        return result

def get_huff_articles(webdriver):
    location = webdriver.current_url
    result = []
    hrefs = set([])
    anchors = webdriver.find_elements_by_class_name('yr-card-headline')
    #anchors.append(webdriver.find_elements_by_class_name('yr-card-image'))
    for anchor in anchors:
        href = anchor.get_attribute('href')
        href = urljoin(location, href)
        if not href:
            continue
        host = urlparse(href).hostname
        if href not in hrefs:
            hrefs.add(href)
            result.append(anchor)
    print(hrefs)
    try:
        return result[0:3]
    except:
        return result

def get_slate_articles(webdriver):
    location = webdriver.current_url
    result = []
    hrefs = set([])
    anchors = webdriver.find_elements_by_class_name('story-card__link')
    #anchors.append(webdriver.find_elements_by_class_name('story_teaser__cta'))
    for anchor in anchors:
        href = anchor.get_attribute('href')
        if not href:
            continue
        host = urlparse(href).hostname
        if href not in hrefs:
            hrefs.add(href)
            result.append(anchor)
    print(hrefs)
    try:
        return result[0:3]
    except:
        return result

def get_huff_articles(webdriver):
    location = webdriver.current_url
    result = []
    hrefs = set([])
    anchors = webdriver.find_elements_by_tag_name('a')
    for anchor in anchors:
        href = anchor.get_attribute('href')
        href = urljoin(location, href)
        if not href:
            continue
        host = urlparse(href).hostname
        if host.find('clips') == 1:
            if href not in hrefs:
                hrefs.add(href)
                result.append(anchor)
    print(hrefs)
    try:
        return result[0:3]
    except:
        return result


def get_ac_articles(webdriver):
    location = webdriver.current_url
    result = []
    hrefs = set([])
    anchors = webdriver.find_elements_by_tag_name('a')
    for anchor in anchors:
        href = anchor.get_attribute('href')
        if not href:
            continue
        host = urlparse(href).hostname
        if host.find('articles') == 1:
            if href not in hrefs:
                hrefs.add(href)
                result.append(anchor)
    print(hrefs)
    try:
        return result[0:3]
    except:
        return result

def get_ac_articles(webdriver):
    location = webdriver.current_url
    result = []
    hrefs = set([])
    anchors = webdriver.find_elements_by_tag_name('a')
    for anchor in anchors:
        href = anchor.get_attribute('href')
        if not href:
            continue
        host = urlparse(href).hostname
        if host.find('2019') == 1:
            if href not in hrefs:
                hrefs.add(href)
                result.append(anchor)
    print(hrefs)
    try:
        return result[0:3]
    except:
        return result

def get_bloomberg_articles(webdriver):
    location = webdriver.current_url
    result = []
    hrefs = set([])
    anchors = webdriver.find_elements_by_tag_name('a')
    for anchor in anchors:
        href = anchor.get_attribute('href')
        if not href:
            continue
        host = urlparse(href).hostname
        if host.find('articles') == 1:
            if href not in hrefs:
                hrefs.add(href)
                result.append(anchor)
    print(hrefs)
    try:
        return result[0:3]
    except:
        return result

def get_economist_articles(webdriver):
    location = webdriver.current_url
    result = []
    hrefs = set([])
    anchors = webdriver.find_elements_by_class_name('teaser__link')
    for anchor in anchors:
        href = anchor.get_attribute('href')
        if not href:
            continue
        host = urlparse(href).hostname
        if href not in hrefs:
            hrefs.add(href)
            result.append(anchor)
    print(hrefs)
    try:
        return result[0:3]
    except:
        return result

def get_wsj_articles(webdriver):
    location = webdriver.current_url
    result = []
    hrefs = set([])
    anchors = webdriver.find_elements_by_class_name('wsj_headline_link')
    for anchor in anchors:
        href = anchor.get_attribute('href')
        if not href:
            continue
        host = urlparse(href).hostname
        if href not in hrefs:
            hrefs.add(href)
            result.append(anchor)
    print(hrefs)
    try:
        return result[0:3]
    except:
        return result

def get_all_rec(webdriver):
    location = webdriver.current_url
    result = []
    hrefs = set([])
    anchors = webdriver.find_elements_by_class_name('fixed-recipe-card__title-link')
    for anchor in anchors:
        href = anchor.get_attribute('href')
        if not href:
            continue
        host = urlparse(href).hostname
        if href not in hrefs:
            hrefs.add(href)
            result.append(anchor)
    print(hrefs)
    try:
        return result[0:3]
    except:
        return result

def get_all_rec(webdriver):
    location = webdriver.current_url
    result = []
    hrefs = set([])
    anchors = webdriver.find_elements_by_class_name('fixed-recipe-card__title-link')
    for anchor in anchors:
        href = anchor.get_attribute('href')
        if not href:
            continue
        host = urlparse(href).hostname
        if href not in hrefs:
            hrefs.add(href)
            result.append(anchor)
    print(hrefs)
    try:
        return result[0:3]
    except:
        return result

def get_cookingnyt(webdriver):
    location = webdriver.current_url
    result = []
    hrefs = set([])
    anchors = webdriver.find_elements_by_class_name('card-recipe-info')
    for anchor in anchors:
        href = anchor.get_attribute('href')
        if not href:
            continue
        host = urlparse(href).hostname
        if href not in hrefs:
            hrefs.add(href)
            result.append(anchor)
    print(hrefs)
    try:
        return result[0:3]
    except:
        return result
