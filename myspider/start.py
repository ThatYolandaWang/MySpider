import platform
from scrapy import cmdline
import os
#cmdline.execute('scrapy crawl itcast'.split())

sysstr = platform.system()
if(sysstr =="Windows"):
    print ("Call Windows cmdline")
    cmdline.execute('scrapy crawl OtodomSpider'.split())
elif(sysstr == "Linux"):
    print ("Call Linux tasks")
    os.system("scrapy crawl OtodomSpider")
else:
    print ("Other System tasks")