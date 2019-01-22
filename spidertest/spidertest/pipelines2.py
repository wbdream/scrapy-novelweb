# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.conf import settings
class SpidertestPipeline(object):

    # def open_spider(self,spider):
    #     host=settings['MONGODB_HOST']
    #     port=settings['MONGODB_PORT']
    #     db_name=settings['MONGODB_DBNAME']
    #     client=pymongo.MongoClient(host=host,port=port)
    #     db=client[db_name]
    #     self.post=db[settings['MONGODB_DOCNAME']]
    #     print(333333333333333333333333333)
    def process_item(self, item, spider):

        '''
        将爬取的信息保存到mysql
        '''
        # 将item里的数据拿出来
        url=item['href']
        name=item['name']
        author=item['author']

        # 和本地的newsDB数据库建立连接
        db = pymysql.connect(
            host='localhost',  # 连接的是本地数据库
            user='root',  # 自己的mysql用户名
            passwd='123',  # 自己的密码
            db='newsDB',  # 数据库的名字
            charset='utf8mb4',  # 默认的编码方式：
            cursorclass=pymysql.cursors.DictCursor)
        try:
            # 使用cursor()方法获取操作游标
            cursor = db.cursor()
            # SQL 插入语句
            sql = "INSERT INTO NEWS(url,novelName,author) \
               VALUES ('%s', '%s', '%s')" % (url,name,author)
            print(sql)
            # 执行SQL语句
            cursor.execute(sql)
            # 提交修改
            db.commit()
        finally:
            # 关闭连接
            db.close()
        return item

            # data={
            #     'url':item['href'],
            #     'name':item['name'],
            #     'author':item['author']
            # }
            # self.post.insert(data)
            # return item
# class ChapterPipeline(object):
#
#     def open_spider(self,spider):
#         # host=settings['MONGODB_HOST']
#         # port=settings['MONGODB_PORT']
#         # db_name=settings['MONGODB_DBNAME']
#         client=pymongo.MongoClient(host='127.0.0.1',port=27017)
#         db=client['scrapy']
#         self.post=db['chapter']
#         print(333333333333333333333333333)
#     def process_item(self, chapter, spider):
#         print(chapter['href'],chapter['name'],chapter['chapterName'],'++++++++++++++')
#         data2={
#             'url':chapter['href'],
#             'name':chapter['name'],
#             'chapterName':chapter['chapterName']
#         }
#         self.post.insert(data2)
#         return chapter

