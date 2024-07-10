# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import codecs
import json

class MyspiderPipeline:
    def __init__(self):
 #       self.f = None
        self.file = codecs.open('mytest.csv', 'wb', encoding='utf-8')

    def open_spider(self, spider):
        print('open spider')
        
 #       self.f = open('./test.csv', mode='a', encoding='utf-8')

    def process_item(self, item, spider):
        print('start spider')
        line = json.dumps(dict(item)) + "\n" 

        self.file.write(f'{item["name"]}; {item["price"]}; {item["room"]}; {item["size"]}; {item["unit"]}; {item["floor"]}; {item["address"]}\n')
        return item

    def close_spider(self, spider):
        print('close spider')