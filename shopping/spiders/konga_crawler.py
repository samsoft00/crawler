# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
from scrapy.selector import Selector
from scrapy import log

from shopping.items import ShoppingItem
from shopping.items import KongaItem


class KongaCrawlerSpider(scrapy.Spider):
    name = 'konga_crawler'
    allowed_domains = ['konga.com']

    start_urls = ('http://www.konga.com/',)

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    #rename parse_item to parse {category-main-title}
    def parse(self, response): 

        categories = Selector(response).xpath('//div[@class="category-list"]')

        for category in categories:
            subcat = category.xpath('//ul[@class="sub-category-list"]')

            for subcat_lists in subcat:
                cat_link = subcat_lists.xpath('li/a/@href').extract()

                # self.logger.info(cat_link)

                #follow the link
                for link in cat_link:
                    # log.msg(link, level=log.INFO)
                    # self.logger.info(cat_link)
                    yield scrapy.http.Request(link, callback=self.parse_product)

        #i = ShoppingItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        #return i


    def parse_product(self, response):
        each_item = Selector(response).xpath('//div[@class="product-image-wrap"]')

        for item in each_item:
            links = item.xpath('a[@class="product-image"]/@href').extract()
            
            for link in links:

                yield scrapy.http.Request(link, callback=self.parse_kongaitem)



    def parse_kongaitem(self, response):
        i = KongaItem()#'//span[@itemprop="name"]/text()')[0]
        
        i['product_url'] = response.url#xpath('div[@class="product-name"]')
        i['product_name'] = response.xpath('//div[@class="product-name"]/h1/span/text()').extract()[0]
        i['product_img'] = response.xpath('//img[@itemprop="image"]/@src').extract()[0]
        i['product_price'] = response.xpath('//span[@class="price"]/text()').extract()[0]
        i['product_details'] = response.xpath('//div[@class="long-description"]/div/p/text()').extract()
        self.logger.info(i)

        yield i;