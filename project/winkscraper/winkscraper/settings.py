# -*- coding: utf-8 -*-

# Scrapy settings for winkscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import sys
import requests
from bs4 import BeautifulSoup

def get_proxy():

    url = "https://github.com/clarketm/proxy-list/blob/master/proxy-list.txt"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    dict = {"https": list(map(lambda x: x[0] + x[1], list(
        zip(map(lambda x: x.text, soup.findAll("td")[::1]), map(lambda x: x.text, soup.findAll("td")[1::1])))))}
    proxyList = dict["https"]

    del proxyList[0:18]
    del proxyList[-3::]

    for i in range(0, len(proxyList) - 1):

        theIndexOfTheGap = str(proxyList[i]).find(" ")
        theStringProxy = str(proxyList[i])
        lengthOfTheStringProxy = len(theStringProxy)
        charactersToErase = lengthOfTheStringProxy - theIndexOfTheGap
        newString = theStringProxy.replace(theStringProxy[-charactersToErase::], "")
        proxyList[i] = newString

    return proxyList[1::2]

proxies = get_proxy()

ROTATING_PROXY_LIST = proxies

BOT_NAME = 'winkscraper'

SPIDER_MODULES = ['winkscraper.spiders']
NEWSPIDER_MODULE = 'winkscraper.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'winkscraper (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Splash...

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 4
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'winkscraper.middlewares.WinkscraperSpiderMiddleware': 543,
#}

# Enable SplashDeduplicateArgsMiddleware by adding it to SPIDER_MIDDLEWARES in your settings.py...

# Set a custom DUPEFILTER_CLASS...

# If you use Scrapy HTTP cache then a custom cache storage backend is required. scrapy-splash provides a subclass of scrapy.contrib.httpcache.FilesystemCacheStorage...

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'winkscraper.middlewares.WinkscraperDownloaderMiddleware': 543,
#}

#PROXY_POOL_ENABLED = True

DOWNLOAD_DELAY = 5

#ROTATING_PROXY_BACKOFF_BASE = 50

ROTATING_PROXY_PAGE_RETRY_TIMES = 500

COOKIES_ENABLED = False

DOWNLOAD_TIMEOUT = 50

#RETRY_ENABLED = True

#RETRY_TIMES = 100

# Enable the Splash middleware by adding it to DOWNLOADER_MIDDLEWARES in your settings.py file and changing HttpCompressionMiddleware priority...

DOWNLOADER_MIDDLEWARES = {
    # ...
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    # ...
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'winkscraper.pipelines.WinkscraperPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


