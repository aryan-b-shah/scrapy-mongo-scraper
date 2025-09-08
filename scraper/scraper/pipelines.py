import os
from pymongo import MongoClient
from dotenv import load_dotenv
from scrapy.exceptions import NotConfigured

class MongoPipeline:
    def __init__(self, mongo_uri, mongo_db, collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection
        self.client = None
        self.collection = None

    @classmethod
    def from_crawler(cls, crawler):
        load_dotenv()
        uri = os.getenv("MONGODB_URI") or crawler.settings.get("MONGODB_URI")
        db = os.getenv("MONGODB_DB") or crawler.settings.get("MONGODB_DB", "scrapy_demo")
        col = os.getenv("MONGODB_COLLECTION") or crawler.settings.get("MONGODB_COLLECTION", "quotes")

        if not uri:
            raise NotConfigured("MONGODB_URI is not set (in .env or settings).")

        return cls(uri, db, col)

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.collection = self.client[self.mongo_db][self.collection_name]
        # Compound index to avoid duplicates (text + author)
        self.collection.create_index([("text", 1), ("author", 1)], unique=True)

    def close_spider(self, spider):
        if self.client:
            self.client.close()

    def process_item(self, item, spider):
        doc = dict(item)
        self.collection.update_one(
            {"text": doc.get("text"), "author": doc.get("author")},
            {"$set": doc},
            upsert=True,
        )
        return item
