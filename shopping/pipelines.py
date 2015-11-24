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
					proDetails = ""
					pro_details = item['product_details']

					#Check if product details is a list
					if type(pro_details) is list:
						proDetails = '\n '.join(detail for detail in pro_details)
						# for d in pro_details:
						# 	proDetails+= "\n"+d.strip()
					else:
						proDetails+= pro_details


					ShoppingDb.create(
						name=item['product_name'].strip(),
						url=item['product_url'], 
						brand=item['product_brand'][0].strip(), 
						img=item['product_img'],
						price=item['product_price'],
						category=item['product_category'].strip(),
						site=item['product_site'],
						details=proDetails)

				except IntegrityError:
					existingData = ShoppingDb.get(url=item['product_url'])
					existingData.name = item['product_name'].strip()
					existingData.brand = item['product_brand'][0].strip()
					existingData.img = item['product_img']
					existingData.price = item['product_price']
					existingData.category = item['product_category'].strip()
					existingData.site = item['product_site']
					existingData.details = proDetails#item['product_details']
					existingData.save()

			return item


class ShoppingDb(Model):
		name = TextField()
		url = CharField(max_length=150, unique=True)
		brand = TextField()
		img = CharField(max_length=200)
		price = CharField(max_length=50)
		category = CharField(max_length=100)
		site = CharField(max_length=50)
		details = TextField()
		timestamp = DateTimeField(default=datetime.datetime.now)

		class Meta:
			database = mysql_db