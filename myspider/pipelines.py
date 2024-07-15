# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import codecs
import json
import requests
import os
from datawrite import DBWrite,CSVWrite
import hashlib
from config import config
import csv

class MyspiderPipeline:
    def __init__(self):
        cfg = config()
        #self.datawrite = DBWrite(cfg.get_db_ip(), cfg.get_db_port(), cfg.get_db_num())
        self.datawrite = CSVWrite('result1.csv')

    def open_spider(self, spider):
        print('open spider')
        self.datawrite.open()
        self.filename = os.path.abspath(os.path.dirname(__file__)) + '\\..\\result.csv'

    def process_item(self, item, spider):
        print('get item', item['id'])
        self.datawrite.write(dict(item))
        # print(md.digest().hex())
        return item

    def close_spider(self, spider):
        self.datawrite.close()
        print('close spider')