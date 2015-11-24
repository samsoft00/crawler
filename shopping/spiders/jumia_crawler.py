# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from shopping.items import ProductItem


class JumiaCrawlerSpider(CrawlSpider):
    name = 'jumia_crawler'
    allowed_domains = ['jumia.com.ng']
    start_urls = [
        'https://www.jumia.com.ng/digital-cameras/',
        'https://www.jumia.com.ng/laptops/',
        'https://www.jumia.com.ng/phones-tablets/',
        ]

    rules = (
        Rule(LinkExtractor(allow=r'\?viewType=listView&page=[0-9]'), callback='parse_product', follow=True),
    )

    def parse_start_url(self, response):
        return self.parse_product(response)

    def parse_product(self, response):
        products = Selector(response).xpath('//div[@class="sku -gallery"]/a/@href').extract()

        for product in products:
            # self.logger.info(product)

            yield scrapy.http.Request(product, callback=self.parse_jumiaItem)


    def parse_jumiaItem(self, response):
        i = ProductItem()#'//span[@itemprop="name"]/text()')[0]

        self.logger.info(response.url)

        i['product_url'] = response.url
        i['product_brand'] = response.xpath('//p[@class="sub-title"]/a/text()').extract()
        i['product_name'] = response.xpath('//div[@class="details -validate-size"]/h1/text()').extract()[0]
        i['product_img'] = response.xpath('//div[@id="thumbs-slide"]/a/img/@alt').extract()[0]
        i['product_price'] = response.xpath('//div[@class="price-box"]/span/span/text()').extract()[1]
        i['product_details'] = response.xpath('//div[@class="list -features -compact -no-float"]/ul/li/text()').extract()
        i['product_category'] = response.xpath('//nav[@class="osh-breadcrumb"]/ul/li/a/text()').extract()[2]
        i['product_site'] = 'jumia'
        self.logger.info(response)

        yield i;