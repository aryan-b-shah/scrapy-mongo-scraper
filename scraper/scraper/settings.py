BOT_NAME = "scraper"
SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

ROBOTSTXT_OBEY = True
USER_AGENT = "NisargScraperBot/1.0 (+https://github.com/your-username)"

DOWNLOAD_DELAY = 0.25
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5
AUTOTHROTTLE_MAX_DELAY = 5
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = "httpcache"

ITEM_PIPELINES = {
    "scraper.pipelines.MongoPipeline": 300,
}

# Defaults can be overridden by .env
MONGODB_URI = None
MONGODB_DB = "scrapy_demo"
MONGODB_COLLECTION = "quotes"

# Export a JSON artifact for the repo
FEEDS = {
    "output/quotes.json": {"format": "json", "overwrite": True},
}
