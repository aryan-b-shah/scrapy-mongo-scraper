import scrapy
from ..items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    custom_settings = {
        "DOWNLOAD_DELAY": 0.25,
        "AUTOTHROTTLE_ENABLED": True,
    }

    def parse(self, response):
        for quote_sel in response.css(".quote"):
            item = QuoteItem()
            item["text"] = quote_sel.css(".text::text").get()
            item["author"] = quote_sel.css(".author::text").get()
            item["tags"] = quote_sel.css(".tag::text").getall()
            item["source_url"] = response.url
            yield item

        next_href = response.css("li.next a::attr(href)").get()
        if next_href:
            yield response.follow(next_href, callback=self.parse)
