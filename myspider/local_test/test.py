
import requests
from requests_file import FileAdapter
from lxml import etree
import redis
import hashlib
import csv
import os
import re
import json

def readredis():
    redisPool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, decode_responses=True)
    rClient = redis.Redis(connection_pool=redisPool)
    keynum = len(rClient.keys('*'))
    print('total key:', keynum)
    print(rClient.keys('*'))

def writedb(key, value):
    redisPool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, decode_responses=True)
    rClient = redis.Redis(connection_pool=redisPool)
    print('write in db')
    rClient.set(key, value)

def request():
    s = requests.Session()
    s.mount('file://', FileAdapter())
    response = s.get(url="file:////D:/Project/myspider/myspider/local_test/Strona 2 - Mieszkania na sprzedaż_ Mokotów, Warszawa _ Otodom.pl.html")

    html = response.text
    selects = etree.HTML(html)

    apartments = selects.xpath('//section[@class="eeungyz1 css-hqx1d9 e12fn6ie0"]')
    page = selects.xpath('//div[@class="css-18budxx e1h66krm0"]')[0]
    total_page = int(selects.xpath('//div[@class="css-18budxx e1h66krm0"]/ul/li[last()-1]')[0].text)
    print('page', total_page)
    i = 0
    for apartment in apartments:
        if i >= total_page:
            break

    #    node = apartment.css('dl.css-uki0wd e1clni9t1')
        
        price = apartment.xpath('.//div[@class="css-13gthep eeungyz2"]/div[@class="css-fdwt8z e1nxvqrh0"]/span')[0].text
        address = apartment.xpath('.//div[@class="css-13gthep eeungyz2"]/div[@class="css-12h460e e1nxvqrh1"]/p')[0].text
        ddimp = apartment.xpath('.//dd')
        count = len(ddimp)
        combine = ''
        room = combine.join(apartment.xpath('.//dd[1]')[0].text)
        sizenode = apartment.xpath('.//dd[3]')
        size = combine.join(apartment.xpath('.//dd[2]')[0].text)
        unit = combine.join(apartment.xpath('.//dd[3]')[0].text)
        i+=1

        data = 'count'+ count+ 'room'+ room+ 'size'+ size+ 'unit'+ unit

        md =  hashlib.md5()
        md.update(data)

        writedb(md.digest(), data)
        print(md.digest(), data)


def parse_json():
    item={}
    price_data = {
        "data": {
            "adAvmData": {
                "lowerPredictionPrice": 1.2773376e+06,
                "lowerPredictionPricePerM": 20275.2,
                "predictionPrice": 1.419264e+06,
                "upperPredictionPrice": 1.5611904e+06,
                "upperPredictionPricePerM": 24780.8,
                "__typename": "AdvertAutomatedValuationModel",
                "__typename": "AdvertAutomatedValuationModel"
            }
        }
    }

    if 'lowerPredictionPrice' in price_data['data']['adAvmData']:  
        print(price_data['data']['adAvmData']['lowerPredictionPrice'])
        item['lowerPredictionPrice']=price_data['data']['adAvmData']['lowerPredictionPrice']

    print(item.keys())

def parse_num():
    price_text_org = "1 009 949,88 €"
    #检查带zł
    pln_unit = 'zł'
    euro_unit = '€'
    exchage_rate = 4.29
    #单位
    if str.find(price_text_org, pln_unit) > 0 or str.find(price_text_org, euro_unit) > 0:
        price_num_list = re.findall(r"\d+\,?\d*", price_text_org)
        price_text = ''.join(price_num_list)
        #数字中的,转.
        if str.find(price_text, ',')>0:
            price_text = price_text.replace(',', '.')
        price_value = float(price_text)
        
        if str.find(price_text_org, euro_unit) > 0:
            price_value = price_value * exchage_rate
        
    print(price_value)

if __name__=="__main__":
    print("start")

#    parse_json()

    data = '{\"label\": \"rent\",\"values\": [\"750 zł\"],\"unit\": \"\",\"__typename\": \"AdditionalInfo\"}'

    data_json = json.loads(data)

    print(data_json['values'][0])

    