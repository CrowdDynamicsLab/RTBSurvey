## Checking out this repository
We are using OpenWPM as a submodule, so after cloning this repository, cd into the directory and type `git submodule update --init OpenWPM/` then you will probably have to cd into the OpenWPM directory and `git pull origin master`. This may cause problems for you if you don't have ssh set up with Github. See these two pages to do this: [here](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) and [here](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/)

You will then have to install OpenWPM locally (this will likely be hard to do on anything but Linux)
To do this, cd into the OpenWPM directory and run both `install.sh` and `install-dev.sh`

## How to specify crawling behavior
We support a limited range of crawling behaviors at the moment, but that means the instructions will be simple. 

A crawl is specified with a [CrawlStrategy](https://github.com/CrowdDynamicsLab/RTBSurvey/blob/0f47f7b489a41e0b8c2c4d9640633f8c8ab627ae/CrawlStrategy.py#L13) object. To create one of these objects you will pass arguments to its constructor. The first argument is the name of the crawling profile, make it something semi descriptive. 

A crawl can visit a fixed list of pages or alternatively visit a landing page from which it derives other pages to visit. 

The fixed list of pages is literally just a Python list of strings specifying which pages to visit. It will then be passed as the second argument to the CrawlStrategy constructor.

To specify landing page and derivation, you need to define a function that takes as input a [Selenium webdriver](https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.remote.webdriver) and outputs a list of Selenium WebElements. You get these kinds of objects by using the webdriver's selectors. [Here](https://github.com/CrowdDynamicsLab/RTBSurvey/blob/0f47f7b489a41e0b8c2c4d9640633f8c8ab627ae/Scheduler.py#L5) is an example of such a function for extracting urls from Reddit. Do this for each landing page you wish to crawl. Then make a dictionary with keys corresponding the URL of the landing page and values corresponding to the name of the function specified above. [Here](https://github.com/CrowdDynamicsLab/RTBSurvey/blob/0f47f7b489a41e0b8c2c4d9640633f8c8ab627ae/Scheduler.py#L36) is an example. This will be passed as the third argument to the constructor. 

Finally, if you want the crawl to have specific time of day or time between crawls restrictions you can specify those. We have sensible defaults in place if not. This dictionary should have a key for `crawl_interval` with an integer value corresponding to the minimum number of minutes between crawls, a key for `time_of_day_min` and a string like `00:10:40` as the value which is the minimum time of day where crawling is allowed, likewise a key can be specified for `time_of_day_max`. This dictionary or nothing in the case that we don't wan to specify restrictions beyond the default is passed as the fourth argument to the constructor. 

[Here](https://github.com/CrowdDynamicsLab/RTBSurvey/blob/0f47f7b489a41e0b8c2c4d9640633f8c8ab627ae/Scheduler.py#L35) is a fully working example that creates a profile called `substantive_news` which visits 3 fixed pages and uses 3 subreddits as landing pages. It can only crawl between 8 and 10pm and won't crawl if this profile has crawled in the last 13 hours.