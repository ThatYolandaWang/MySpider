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

class MyspiderPipeline:
    def __init__(self):
 #       self.f = None
        if os.path.isfile('mytest.csv'):
            os.remove('mytest.csv')
        
        open("mytest.csv","w+").close()
        self.file = codecs.open('mytest.csv', 'rb+', encoding='utf-8')

    def open_spider(self, spider):
        print('open spider')
        
 #       self.f = open('./test.csv', mode='a', encoding='utf-8')

    def process_item(self, item, spider):
        print('start spider')
        line = json.dumps(dict(item)) + "\n" 

        self.file.write(f'{item["name"]}; {item["price"]}; {item["room"]}; {item["size"]}; {item["unit"]}; {item["floor"]}; {item["address"]}\n')
        return item

    def close_spider(self, spider):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer YOUR_API_KEY'
        }
        url = 'https://1711ed8d-2402-4c9e-83d0-68568418aac9.mock.pstmn.io'

        files = {'file':self.file}
        response = requests.post(url, files=files)

        self.file.close()
        print('close spider')