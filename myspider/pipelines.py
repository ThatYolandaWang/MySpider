# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import requests
import os
from myspider.datawrite import DBWrite,CSVWrite
from myspider.config import config

class MyspiderPipeline:
    def __init__(self):
        cfg = config()
        #self.datawrite = DBWrite(cfg.get_db_ip(), cfg.get_db_port(), cfg.get_db_num())
        self.datawrite = CSVWrite('result.csv')

    def open_spider(self, spider):
        print('open spider')
        self.datawrite.open()

    def process_item(self, item, spider):
        print('get item', item['id'])
        self.datawrite.write(dict(item))
        # print(md.digest().hex())
        return item

    def close_spider(self, spider):
        self.datawrite.close()
        print('close spider')