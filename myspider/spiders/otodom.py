import scrapy
from lxml import etree
from myspider.items import OtodomItem


class OtodomSpider(scrapy.Spider):
    name = "OtodomSpider" #蜘蛛标识
    allowed_domains = ['otodom.pl']#["allegro.pl"]
    start_urls = ['https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/warszawa/mokotow?viewType=listing']#("https://allegro.pl/listing?string=iphone15",) #["https://itcast.cn"]
    headers = {
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection":"keep-alive",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    current_page = 1
    total_page = 1

    def start_requests(self):
 #       url = 'https://www.otodom.pl/'
        yield scrapy.Request(self.start_urls[0], headers=self.headers)

    def parse(self, response):

        html = response.text
        selects = etree.HTML(html)

        apartments = selects.xpath('//section[@class="eeungyz1 css-hqx1d9 e12fn6ie0"]')

        i = 0
        if self.current_page > 1:#self.total_page:
            return
        
        if self.current_page == 1:
            page = selects.xpath('//div[@class="css-18budxx e1h66krm0"]')[0]
            #查询总页数
            self.total_page = int(page.xpath('.//ul/li[last()-1]')[0].text)
            print("totel page:", str(self.total_page))
            item = OtodomItem()
            item['price'] = 'price'
            item['name'] = 'name'
            item['room'] = 'room'
            item['size'] = 'size'
            item['floor'] = 'floor'
            item['unit'] = 'unit'
            item['address'] = 'address'
            yield item

        for apartment in apartments:
            item = OtodomItem()
            item['price'] = apartment.xpath('.//div[@class="css-13gthep eeungyz2"]/div[@class="css-fdwt8z e1nxvqrh0"]/span')[0].text
            item['name'] = apartment.xpath('.//div[@class="css-13gthep eeungyz2"]/a/p')[0].text
            item['address'] = apartment.xpath('.//div[@class="css-13gthep eeungyz2"]/div[@class="css-12h460e e1nxvqrh1"]/p')[0].text
            
            count = len(apartment.xpath('.//dd'))
            combine = ''
            if count >=1 :
                item['room'] = combine.join(apartment.xpath('.//dd[1]')[0].text)
            if count >=2:
                item['size'] = combine.join(apartment.xpath('.//dd[2]/text()'))
            if count >=3:
                item['unit'] = combine.join(apartment.xpath('.//dd[3]/text()'))
            if count >=4:
                item['floor'] = combine.join(apartment.xpath('.//dd[4]/text()'))
            print(item)
            i+=1
            yield item

        print("currentpage:", self.current_page, self.total_page)

        next_url = self.start_urls[0]+'/&page='+str(self.current_page)
        self.current_page+=1

        yield scrapy.Request(next_url, callback=self.parse, headers=self.headers)
        