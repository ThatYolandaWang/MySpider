# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class OtodomItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()

    address = scrapy.Field()
    linkage = scrapy.Field()

    id = scrapy.Field()
    # detail = scrapy.Field()
    # predict_price = scrapy.Field()

    #详情
    createdAt = scrapy.Field()
    modifiedAt = scrapy.Field()
    Build_year = scrapy.Field()
    Building_floors_num = scrapy.Field()
    Building_ownership = scrapy.Field()
    Building_type = scrapy.Field()
    room = scrapy.Field()
    size = scrapy.Field()
    unit = scrapy.Field()
    floor = scrapy.Field()
    city = scrapy.Field()
    Construction_status = scrapy.Field()
    Energy_certificate = scrapy.Field()
    Rent = scrapy.Field()
    hidePrice = scrapy.Field()
    lat = scrapy.Field()
    long = scrapy.Field()
    district = scrapy.Field()

    lowerPredictionPrice = scrapy.Field()
    lowerPredictionPricePerM = scrapy.Field()
    predictionPrice = scrapy.Field()
    upperPredictionPrice = scrapy.Field()
    upperPredictionPricePerM = scrapy.Field()