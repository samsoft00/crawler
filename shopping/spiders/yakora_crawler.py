# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from shopping.items import ShoppingItem

from selenium import webdriver


class YakoraCrawlerSpider(CrawlSpider):
    name = 'yakora_crawler'
    allowed_domains = ['yakora.com']
    start_urls = [
        'http://www.yakora.ng/1690-laptops/',
        'http://www.yakora.ng/1622-mobile-phones/',
        'http://www.yakora.ng/1679-computer-peripherals',
        'http://www.yakora.ng/2206-top-televisions'
    ]

    rules = (
        Rule(LinkExtractor(allow=r'#/page-2'), callback='parse_product', follow=True),
    )

    def __init__(self):
        self.driver = webdriver.Firefox()
        

    def parse_start_url(self, response):
        return self.parse_product(response)    


    def parse_product(self, response):
        products = Selector(response).xpath('//div[@class="pro_first_box"]/a/@href').extract()
        i = ShoppingItem()

        self.logger.info(response)


        return i
