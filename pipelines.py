import scrapy
from pymongo import MongoClient
import os
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline
from datetime import datetime

class LeroymerlinPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroy_merlin

    def process_item(self, item, spider):
        item['details'] = dict(zip(item['details_keys'], item['details_items']))
        item['query'] = spider.query
        item['updated'] = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        del item['details_keys'], item['details_items']

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item

class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        return 'file/' + info.spider.query + '/' + os.path.basename(urlparse(request.url).path)

    def item_completed(self, results, item, info):
        if results:
            item['photo'] = [itm[1] for itm in results if itm[0]]

        return item




