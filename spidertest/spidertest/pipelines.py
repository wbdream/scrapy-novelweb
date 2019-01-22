# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
class SpidertestPipeline(object):

    def open_spider(self,spider):
        host=settings['MONGODB_HOST']
        port=settings['MONGODB_PORT']
        db_name=settings['MONGODB_DBNAME']
        client=pymongo.MongoClient(host=host,port=port)
        db=client[db_name]
        self.post=db[settings['MONGODB_DOCNAME']]
    def process_item(self, item, spider):
        data={
            'url':item['href'],
            'name':item['name'],
            'chapterName':item['chapterName']
        }
        self.post.insert(data)
        return item


class ChapterPipeline(object):

    def open_spider(self,spider):
        # host=settings['MONGODB_HOST']
        # port=settings['MONGODB_PORT']
        # db_name=settings['MONGODB_DBNAME']
        client=pymongo.MongoClient(host='127.0.0.1',port=27017)
        db=client['scrapy']
        self.post=db['chapter']
        print(333333333333333333333333333)
    def process_item(self, item, spider):
        print(item['href'],item['name'],item['chapterName'],'++++++++++++++')
        data2={
            'url':item['href'],
            'name':item['name'],
            'chapterName':item['chapterName']
        }
        self.post.insert(data2)
        return item
