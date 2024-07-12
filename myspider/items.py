# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class OtodomItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    room = scrapy.Field()
    size = scrapy.Field()
    unit = scrapy.Field()
    floor = scrapy.Field()
    address = scrapy.Field()
    linkage = scrapy.Field()

    #详情
    id = scrapy.Field()
    detail = scrapy.Field()
    price_range = scrapy.Field()