# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from peewee import *
import datetime

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


mysql_db = MySQLDatabase(
	'shopping', #Database name
	user='root', #Database username
	password='adefioye', #Database password
	host='localhost', # host
	)


class ShoppingPipeline(object):

		def __init__(self):
			mysql_db.connect()
			mysql_db.create_tables([ShoppingDb], safe=True)


		def process_item(self, item, spider):
			valid = True

			for data in item:
				if not data:
					valid = False
					raise DropItem("Missing {0}".format(data))
			if valid:
				try:
					ShoppingDb.create(name=item['product_name'],url=item['product_url'],img=item['product_img'],price=item['product_price'],details=item['product_details'])
				except IntegrityError:
					existingData = ShoppingDb.get(url=item['product_url'])
					existingData.name = item['product_name']
					existingData.img = item['product_img']
					existingData.price = item['product_price']
					existingData.details = item['product_details']
					existingData.save()

			return item


class ShoppingDb(Model):
		name = TextField()
		url = CharField(max_length=150, unique=True)
		img = CharField(max_length=200)
		price = CharField(max_length=50)
		details = CharField(max_length=255)
		timestamp = DateTimeField(default=datetime.datetime.now)

		class Meta:
			database = mysql_db