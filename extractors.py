from urlparse import urlparse, urljoin

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
