# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShoppingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ProductItem(scrapy.Item):
		"""docstring for KongaItem"""
		product_name = scrapy.Field()
		product_img = scrapy.Field()
		product_price = scrapy.Field()
		product_url = scrapy.Field()
		product_brand = scrapy.Field()
		product_details = scrapy.Field()
		product_category = scrapy.Field()
		product_site = scrapy.Field();