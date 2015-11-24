# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from shopping.items import ProductItem


class SmartbuyCrawlerSpider(CrawlSpider):
    name = 'smartbuy_crawler'
    allowed_domains = ['smartbuy.ng']
    start_urls = [
        'http://www.smartbuy.ng/shop-all-categories/mobile-phone-tablets.html',
        ]

    rules = (
        Rule(LinkExtractor(allow=r'\?p=[0-9]'), callback='parse_product', follow=True),
    )

    def parse_start_url(self, response):
        return self.parse_product(response)    

    def parse_product(self, response):
        products = Selector(response).xpath('//div[@class="product-image-area"]/a/@href').extract()

        for product in products:

            self.logger.info(product)

            yield scrapy.http.Request(product, callback=self.parse_smartbuyItem)
        # return i


    def parse_smartbuyItem(self, response):
        i = ProductItem()#'//span[@itemprop="name"]/text()')[0]

        self.logger.info(response.url)
        i['product_url'] = response.url
        i['product_img'] = response.xpath('//img[@class="etalage_thumb_image"]/@src').extract()[0]
        i['product_price'] = response.xpath('//div[@class="price-box"]/span/span/text()').extract()[0]
        i['product_name'] = response.xpath('//div[@class="product-name"]/h1/text()').extract()[0]
        i['product_category'] = response.xpath('//li[@class="category130"]/a/text()').extract()[0]
        pro_description = response.xpath('//div[@class="std"]').extract()[0]

        i['product_details'] = ''#pro_description.xpath('//span')[0]
        i['product_brand'] = str(response.xpath('//div[@class="product-name"]/h1/text()').extract()[0]).split(' ')
        i['product_site'] = 'smartbuy'
        self.logger.info(response)

        yield i;