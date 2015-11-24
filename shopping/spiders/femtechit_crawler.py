# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from shopping.items import ProductItem
from urlparse import urlparse

class FemtechitCrawlerSpider(CrawlSpider):
    name = 'femtechit_crawler'
    allowed_domains = ['femtechit.com']
    start_urls = [
        "http://femtechit.com/digital-cameras",
        "http://femtechit.com/tablets",
        "http://femtechit.com/laptops-notebooks",
        "http://femtechit.com/mobilephones",
        ]

    rules = (
        Rule(LinkExtractor(allow=r'\?page=[0-d+]'), callback='parse_product', follow=True),
    )

    def parse_start_url(self, response):
        return self.parse_product(response)

    def parse_product(self, response):
        products = Selector(response).xpath('//div[@class="image"]/a/@href').extract()

        for product in products:

            self.logger.info(product)
            # url = urlparse(str(product_url))
            yield scrapy.http.Request(product, callback=self.parse_Femtechitem)


    def parse_Femtechitem(self, response):
        i = ProductItem()#'//span[@itemprop="name"]/text()')[0]
        
        i['product_url'] = response.url
        i['product_brand'] = response.xpath('//ul[@class="list-unstyled"]/li/a/text()').extract()
        i['product_name'] = response.xpath('//h1[@class="title-product"]/text()').extract()[0]
        i['product_img'] = response.xpath('//a[@class="info_colorbox"]/img/@src').extract()[0]
        i['product_price'] = response.xpath('//ul[@class="list-unstyled"]/li/span/text()').extract()[0]
        i['product_details'] = response.xpath('//div[@id="tab-description"]/p/text()').extract()
        i['product_category'] = response.xpath('//ul[@class="breadcrumb"]/li/a/text()').extract()[0]
        i['product_site'] = 'femtechit'
        self.logger.info(response)

        yield i;        
