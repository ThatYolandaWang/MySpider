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
from dbwrite import DBWrite
import hashlib
from config import config

class MyspiderPipeline:
    def __init__(self):
        cfg = config()
        self.dbwrite = DBWrite(cfg.get_db_ip(), cfg.get_db_port(), cfg.get_db_num())

    def open_spider(self, spider):
        print('open spider')
        self.dbwrite.connect()

    def process_item(self, item, spider):
        print('start spider')
        line = json.dumps(dict(item))

        # self.file.write(f'{item["name"]}; {item["price"]}; {item["room"]}; {item["size"]}; {item["unit"]}; {item["floor"]}; {item["address"]}\n')
        md =  hashlib.md5()
        md.update(str.encode(line))

        self.dbwrite.write(md.digest().hex(), line)
        print(md.digest().hex())
        return item

    def close_spider(self, spider):
        self.dbwrite.close()
        print('close spider')