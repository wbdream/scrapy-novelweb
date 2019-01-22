# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup
import re
from ..items import SpidertestItem
from ..items import ChapterItem
import time
import os

class BuqugeSpider(scrapy.Spider):
    name = 'buquge'
    allowed_domains = ['biquge5.com']
    start_urls = ['http://www.biquge5.com/xiaoshuodaquan']

    def parse(self, response):
        # print(type(response.text))
        # time.sleep(0.5)
        # text=response.xpath('//div[@class="novellist"]/ul/li/a').extract()
        # text=bs.find_all('li')
        # text=re.findall('<a (.*?)>"(.*?)"<em>(.*?)</em>',response.text,re.S)
        text=re.findall('<a href="(.*?)">(.*?) <em>(.*?)</em>',response.text)
        # for i in text:
        #     # print(type(i))
        #     item = SpidertestItem()
        #     item['href']='http://www.biquge5.com'+i[0]
        #     item['name']=i[1]
        #     item['author']=i[2]
        #     # print(item['author'],item['name'],'******************')
        #     yield item
        # print(1111115556666622222222)
        for i in text:
            item = SpidertestItem()
            item['href']='http://www.biquge5.com'+i[0]
            item['name']=i[1]
            item['author']=i[2]
            isExists = os.path.exists("../novel")
            if not isExists:
                os.makedirs('../novel')
            yield scrapy.Request(url='http://www.biquge5.com'+i[0],callback=self.parse_content)
#小说
    def parse_content(self,response):
        # time.sleep(0.5)
        novel_name=response.xpath('//*[@id="info"]/h1/text()').extract_first()
        jieshao=response.xpath('//*[@id="intro"]/p/text()')
        text=re.findall('<ul class="_chapter">(.*?)</ul>',response.text,re.S)
        chapters = re.findall('<a href="(.*?)\r\n\t\t\t(.*?)">(.*?)</a>', text[0],re.S)
        for item in chapters:
            chapter=ChapterItem()
            chapter['name']=novel_name
            chapter['href']=item[0]+item[1]
            chapter['chapterName']=item[2]
            # isExists = os.path.exists("../novel/" + novel_name)
            # if not isExists:
            #     os.makedirs('../novel/' + novel_name)
            yield chapter
        for item in chapters:
            yield scrapy.Request(url=item[0]+item[1],callback=self.parse_chapterContent)
#章节内容提取
    def parse_chapterContent(self,response):
        time.sleep(0.5)
        sort=response.css('#wrapper > div.content_read > div > div.con_top > a:nth-child(4)::text').extract_first()
        novel_name=response.xpath('//*[@id="wrapper"]/div[5]/div[1]/a[3]/text()').extract_first()
        chapter_name=response.css('#wrapper h1::text').extract_first()
        if '/' in chapter_name:
            chapter_name = re.split('（', chapter_name)
            chapter_name=chapter_name[0]

        bs=BeautifulSoup(response.text,'lxml')
        content = bs.select("#content")
        #创建路劲
        isExists = os.path.exists("../novel/" + sort+'/'+novel_name)
        if not isExists:
            os.makedirs('../novel/' + sort+'/'+novel_name)


        #章节内容
        with open('../novel/' + sort+'/'+novel_name+'/'+chapter_name+'.txt','a+',encoding='utf-8') as f:
            # f.write('wwwwwwww')
            f.write(content[0].get_text())

        # url_first=re.findall('http://(.*?)/(.*?)/(.*?).html',response.url)
        url_first=re.findall('http://(.*?).html',response.url)
        urls=re.split('/',url_first[0])

        url=re.findall('<a href="(.*?).html">下一章</a>',response.text)
        if '_' in url[0]:
            return scrapy.Request(url='http://'+urls[0]+'/'+urls[1]+'/'+url[0]+'.html', callback=self.parse_chapterContent)

        # print(url)
    # def parse_chapterContent2(self,response):
    #
    #     print(response.text)