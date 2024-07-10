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

class TaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    class1 = scrapy.Field()
    class2 = scrapy.Field()

# 这个item是获取具体内容的字段    
class TaobaoDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    sales = scrapy.Field()
    store = scrapy.Field()
    class1 = scrapy.Field()
    class2 = scrapy.Field()
    