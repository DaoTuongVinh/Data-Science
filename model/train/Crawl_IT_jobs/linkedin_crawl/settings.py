BOT_NAME = "linkedin_crawl"

SPIDER_MODULES = ["linkedin_crawl.spiders"]
NEWSPIDER_MODULE = "linkedin_crawl.spiders"



# Obey robots.txt rules
ROBOTSTXT_OBEY = False

## settings.py

SCRAPEOPS_API_KEY = 'c46fa6b4-98a3-49e7-b5d3-15dab5aad820'
SCRAPEOPS_PROXY_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
}


# Add In The ScrapeOps Extension
EXTENSIONS = {
'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500, 
}


# Update The Download Middlewares
DOWNLOADER_MIDDLEWARES = {
'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

HTTPERROR_ALLOWED_CODES =[404,429]
RETRY_HTTP_CODES = [429]

USER_AGENT='Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'