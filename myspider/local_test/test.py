
import requests
from requests_file import FileAdapter
from lxml import etree
import redis
import hashlib


redisPool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, decode_responses=True)
rClient = redis.Redis(connection_pool=redisPool)

def writedb(key, value):
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


if __name__=="__main__":
    print("start")

    data = 'count'

    md =  hashlib.md5()
    md.update(str.encode(data))
    dig = md.digest()
    strdig = dig.hex()
    keynum = len(rClient.keys('*'))
    print('total key:', keynum)
    print(rClient.keys('*'))
    
#    print('check keys ', rClient.get('027cf515d9bc45d9b1502b2282e4c768'))
    # print('set name ', rClient.set('name', 'Zhou'))
    # print('check name value ',rClient.get('name'))
#    request()

