# -*- coding: utf-8 -*-

# Scrapy settings for opaxe project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os
from mysql.connector import connect

BOT_NAME = 'files_finder'

SPIDER_MODULES = ['.spiders']
NEWSPIDER_MODULE = 'spider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'files_finder (+http://www.example.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'opaxe.middlewares.OpaxeSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'opaxe.middlewares.OpaxeDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'opaxe.pipelines.OpaxePipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#
#
#
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600 * 24
HTTPCACHE_DIR = '/tmp/.scrapy/httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [400, 401, 403, 404, 500, 501, 502, 503]
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

REACTOR_THREADPOOL_MAXSIZE = 1000 * 500
CONCURRENT_REQUESTS_PER_DOMAIN = 50
CONCURRENT_ITEMS = 1000 * 3
DOWNLOAD_MAXSIZE = 1024000 * 5  # 5 MB in bytes
LOG_ENABLED = True
LOG_LEVEL = 'INFO'
ROBOTSTXT_OBEY = False
SCHEDULER_PRIORITY_QUEUE = 'scrapy.pqueues.DownloaderAwarePriorityQueue'
COOKIES_ENABLED = False
AJAXCRAWL_ENABLED = True
DNSCACHE_SIZE = 1024000 * 50
RETRY_ENABLED = False
DOWNLOAD_TIMEOUT = 45
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': None,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None
}

DOWNLOAD_HANDLERS = {
    'file': None,
    's3': None,
    'ftp': None
}

# SQS Name to send discovered file links
AWS_SQS_NAME = os.environ.get('AWS_SQS_NAME')

# HTML compression to save
HTML_COMPRESSION_ENABLE = True
HTML_COMPRESSION_LEVEL = 9

# download extensions
FILE_EXTENSIONS = os.environ.get('DOWNLOAD_EXTENSION', 'pdf').split(',')

#  DB Credentials
db_host = os.environ.get('DB_HOST', 'localhost')
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER', 'root')
db_password = os.environ.get('DB_PASSWORD', '')
db_port = os.environ.get('DB_PORT', 3306)

DB_CRED = {'host': db_host, 'database': db_name, 'user': db_user, 'password': db_password, 'port': int(db_port)}
