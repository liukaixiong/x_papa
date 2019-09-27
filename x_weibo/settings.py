# -*- coding: utf-8 -*-

# Scrapy settings for x_papa project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'x_weibo'

SPIDER_MODULES = ['x_weibo.spiders']
NEWSPIDER_MODULE = 'x_weibo.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'x_papa (+http://www.yourdomain.com)'
USER_AGENT = [
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14',
    'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/527 (KHTML, like Gecko, Safari/419.3) Arora/0.6 (Change: )',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1 '
]
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie':'_T_WM=88819513180; ALF=1571883517; SCF=Amp0K_iWqOQXNBAacw3C0u_dVbzxhJVtBjTuuLjNPTIU8hWx_R9rBWZ8hNrMx4RY9OdBmG5hw89iTUXr25S1qB8.; SUB=_2A25wjQ7ZDeThGeNI6VUQ9y3NyzyIHXVQcZKRrDV6PUJbktANLRnjkW1NSJ3XCaB4ggZa0iiZR2KUTAfhHkkbE24g; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFdc7grDhZy8BfuLoHqaYFI5JpX5K-hUgL.Fo-ceoMpS0epeh52dJLoI0YLxKBLBo.LBK5LxKqL1heLB-qLxK-L1K5LB-eLxKBLB.BLBK5LxKnLB-qLBoBLxKqL122LBo2LxKqLB-BL1h.t; SUHB=0wnlkNF2YzH2q2; SSOLoginState=1569291913; MLOGIN=1'
}
CONCURRENT_REQUESTS = 16
#只有这一行代码，其他的是为了方便查找，加上这一行基本上就能解决了
MEDIA_ALLOW_REDIRECTS = True
#
DOWNLOAD_DELAY = 3
DOWNLOADER_MIDDLEWARES = {
    'weibo.middlewares.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None
    ,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None
}
#
# DOWNLOADER_MIDDLEWARES = {
#     'weibo.middlewares.UserAgentMiddleware': None,
#     'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
#     'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None
# }
# ITEM_PIPELINES = {
#     'sina.pipelines.MongoDBPipeline': 300,
# }
# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'x_weibo.middlewares.SWeiboSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'x_weibo.middlewares.SWeiboDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'x_weibo.pipelines.SWeiboPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
