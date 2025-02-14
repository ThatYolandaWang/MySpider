import scrapy
from lxml import etree
from myspider.items import OtodomItem
from myspider.config import config
import json
import requests
import httpx
import re

class OtodomSpider(scrapy.Spider):
    name = "OtodomSpider" #蜘蛛标识
    allowed_domains = ['otodom.pl']#["allegro.pl"]
    headers = {
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection":"keep-alive",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Content-Type":"application/json;charset=utf-8"
    }
    current_page = 1
    total_page = 1
    current_url_index = 0

    cfg = config()
    start_urls = cfg.get_url_list()


    def start_requests(self):
        print('start request in :', self.start_urls[self.current_url_index])
        yield scrapy.Request(self.start_urls[0], headers=self.headers)

    def parse(self, response):
        print("currentpage:", self.current_page, self.total_page)
        html = response.text
        selects = etree.HTML(html)
        apartments = selects.xpath('//section[@class="eeungyz1 css-hqx1d9 e12fn6ie0"]')

        if self.current_page == 1:
            #查询总页数
            self.total_page = int(selects.xpath('//div[@class="css-18budxx e1h66krm0"]/ul/li[last()-1]')[0].text)
            print("totel page:", str(self.total_page))
            # item = OtodomItem()
            # item['price'] = 'price'
            # item['name'] = 'name'
            # item['room'] = 'room'
            # item['size'] = 'size'
            # item['floor'] = 'floor'
            # item['unit'] = 'unit'
            # item['address'] = 'address'
            # yield item

        for apartment in apartments:

            item = OtodomItem()
            combine = ''
            price_text_org = apartment.xpath('.//div[@class="css-13gthep eeungyz2"]/div[@class="css-fdwt8z e1nxvqrh0"]/span')[0].text
            #解析价格数据
            pln_unit = 'zł'
            euro_unit = '€'
            exchage_rate = 4.29
            price_value = 0 #初始化，如果没价格就算0
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

            item['price'] = int(price_value)

            #item['price']
            item['name'] = apartment.xpath('.//div[@class="css-13gthep eeungyz2"]/a/p')[0].text
            detail_url = apartment.xpath('.//div[@class="css-13gthep eeungyz2"]/a/@href')[0]
            if str.find(detail_url, 'http'):
                detail_url = 'https://www.otodom.pl'+ detail_url

            item['linkage'] = detail_url
            item['address'] = apartment.xpath('.//div[@class="css-13gthep eeungyz2"]/div[@class="css-12h460e e1nxvqrh1"]/p')[0].text
 
            yield scrapy.Request(detail_url, callback=self.parse_detail, headers=self.headers, meta={'item':item})
            
#            yield item

        
        
        next_url = ""
        # 如果启用debug，则仅查询一页
        total_page = self.total_page
        if self.cfg.get_test_status == True:
            total_page = 1
        if self.current_page >= total_page:
            if self.current_url_index < len(self.start_urls)-1:
                self.current_page = 1
                self.total_page = 0
                self.current_url_index += 1
                print('start request in :', self.start_urls[self.current_url_index])
                next_url = self.start_urls[self.current_url_index]
        else:
            next_url = self.start_urls[self.current_url_index]+'?page='+str(self.current_page)
            self.current_page+=1
        
        if next_url != '':
            yield scrapy.Request(next_url, callback=self.parse, headers=self.headers)

    def parse_detail(self, response):
        html = response.text
        selects = etree.HTML(html)

        item = response.meta['item']

        #查找对应房屋otodom编号
        script = selects.xpath('//script[@id="__NEXT_DATA__"]')[0].text
        
        data = json.loads(script)

        item['id'] = str(data['props']['pageProps']['ad']['id'])
        # item['detail'] = script
        headers = {
            "Content-Type":"application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }

        request_data = '{\"query\":\"query AdAvmQuery($input: advertAutomatedValuationModelInput!) {\\n  adAvmData: advertAutomatedValuationModel(input: $input) {\\n    ... on AdvertAutomatedValuationModel {\\n      lowerPredictionPrice\\n      lowerPredictionPricePerM\\n      predictionPrice\\n      upperPredictionPrice\\n      upperPredictionPricePerM\\n      __typename\\n    }\\n    ... on AdvertAutomatedValuationModelError {\\n      error\\n      __typename\\n    }\\n    ... on ErrorInternal {\\n      code\\n      message\\n      __typename\\n    }\\n    __typename\\n  }\\n}\",\"operationName\":\"AdAvmQuery\",\"variables\":{\"input\":{\"advertId\":%s,\"currencyTransformation\":\"PLN\"}}}' % item['id']
        
        resp = httpx.post('https://www.otodom.pl/api/query', data = request_data, headers=headers, timeout=10, verify=False)
        
        item = self.parse_script(data,json.loads(resp.text), item)
        # if resp.status_code == 200:
        #     item['predict_price'] = resp.text
        # else:
        #     item['predict_price'] = ''
        
        yield item
    
    def parse_script(self, detail, price_data, item):


        if 'createdAt' in detail['props']['pageProps']['ad']: 
            item['createdAt']= detail['props']['pageProps']['ad']['createdAt']
        
        if 'modifiedAt' in detail['props']['pageProps']['ad']:
            item['modifiedAt']=detail['props']['pageProps']['ad']['modifiedAt']
        
        if 'Build_year' in detail['props']['pageProps']['ad']['target']:
            item['Build_year']=int(detail['props']['pageProps']['ad']['target']['Build_year'])

        if 'Building_floors_num' in detail['props']['pageProps']['ad']['target']:
            item['Building_floors_num']=int(detail['props']['pageProps']['ad']['target']['Building_floors_num'])
        
        if 'Building_ownership' in detail['props']['pageProps']['ad']['target']:
            item['Building_ownership']=','.join(detail['props']['pageProps']['ad']['target']['Building_ownership'])

        if 'Building_type' in detail['props']['pageProps']['ad']['target']:
            item['Building_type']=','.join(detail['props']['pageProps']['ad']['target']['Building_type'])
        if 'Construction_status' in detail['props']['pageProps']['ad']['target']:
            item['Construction_status']=','.join(detail['props']['pageProps']['ad']['target']['Construction_status'])
        if 'Energy_certificate' in detail['props']['pageProps']['ad']['target']:
            item['Energy_certificate']=','.join(detail['props']['pageProps']['ad']['target']['Energy_certificate'])
        if 'Rent' in detail['props']['pageProps']['ad']['target']:
            item['Rent']=detail['props']['pageProps']['ad']['target']['Rent']
        if 'hidePrice' in detail['props']['pageProps']['ad']['target']:       
            item['hidePrice']=detail['props']['pageProps']['ad']['target']['hidePrice']
        if 'lat' in detail['props']['pageProps']['adTrackingData']:      
            item['lat']=detail['props']['pageProps']['adTrackingData']['lat']
        if 'long' in detail['props']['pageProps']['adTrackingData']:        
            item['long']=detail['props']['pageProps']['adTrackingData']['long']

        if 'Area' in detail['props']['pageProps']['ad']['target']:
            item['size']=detail['props']['pageProps']['ad']['target']['Area']
        if 'City' in detail['props']['pageProps']['ad']['target']:
            item['city']=detail['props']['pageProps']['ad']['target']['City']
        if 'Rooms_num' in detail['props']['pageProps']['ad']['target']:
            item['room']=detail['props']['pageProps']['ad']['target']['Rooms_num'][0]
        if 'Price_per_m' in detail['props']['pageProps']['ad']['target']:
            item['unit']=detail['props']['pageProps']['ad']['target']['Price_per_m']
        
        if 'Floor_no' in detail['props']['pageProps']['ad']['target']:
            floor_text = detail['props']['pageProps']['ad']['target']['Floor_no'][0]
            if str.find(floor_text, 'ground_floor')>0:
                item['floor']=0
            else:
                ls_floor = re.findall(r"\d+", floor_text)
                if len(ls_floor)>0:
                    item['floor']=ls_floor[0]

        if 'district' in detail['props']['pageProps']['ad']['location']['address']:
            item['district'] = detail['props']['pageProps']['ad']['location']['address']['district']['name']

        if 'lowerPredictionPrice' in price_data['data']['adAvmData']:  
            item['lowerPredictionPrice'] = price_data['data']['adAvmData']['lowerPredictionPrice']
        if 'lowerPredictionPricePerM' in price_data['data']['adAvmData']:       
            item['lowerPredictionPricePerM']=price_data['data']['adAvmData']['lowerPredictionPricePerM']
        if 'predictionPrice' in price_data['data']['adAvmData']:    
            item['predictionPrice']=price_data['data']['adAvmData']['predictionPrice']
        if 'upperPredictionPrice' in price_data['data']['adAvmData']:        
            item['upperPredictionPrice']=price_data['data']['adAvmData']['upperPredictionPrice']
        if 'upperPredictionPricePerM' in price_data['data']['adAvmData']:       
            item['upperPredictionPricePerM']=price_data['data']['adAvmData']['upperPredictionPricePerM']
        return item