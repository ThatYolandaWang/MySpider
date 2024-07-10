
import requests
from requests_file import FileAdapter
from lxml import etree


s = requests.Session()
s.mount('file://', FileAdapter())
response = s.get(url="file:////D:/Project/myspider/Strona 2 - Mieszkania na sprzedaż_ Mokotów, Warszawa _ Otodom.pl.html")

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
    print('count', count, 'room', room, 'size', size, 'unit', unit)


#node1 = selects.xpath('//dl[@class="css-uki0wd e1clni9t1"]')[0]

#print(node1.xpath('./dd[3]/text()'))
#print(node1.xpath("//dd[3]/text()")[0]+selects.xpath("//dd[3]/text()")[1]+selects.xpath("//dd[3]/text()")[2])

#str = ''
#print(str.join(node1.xpath('./dd[3]/text()')))