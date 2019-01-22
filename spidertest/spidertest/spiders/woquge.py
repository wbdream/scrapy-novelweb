# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup
class WoqugeSpider(scrapy.Spider):
    name = 'woquge'

    allowed_domains = ['www.woquge.com']
    start_urls = ['https://www.woquge.com/xiaoshuodaquan/']

    def parse(self, response):
        print(4555555555555555454)
        text=re.findall('<a href="(.*?)">(.*?)</a>',response.text)

        print(text)
