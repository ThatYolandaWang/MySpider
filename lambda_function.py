import json
import platform
from scrapy import cmdline
import os

print('Loading function')

def lambda_handler(event, context):
    sysstr = platform.system()
    if(sysstr =="Windows"):
        print ("Call Windows cmdline")
        cmdline.execute('scrapy crawl OtodomSpider'.split())
    elif(sysstr == "Linux"):
        print ("Call Linux tasks")
        os.system("scrapy crawl OtodomSpider")
    else:
        print ("Other System tasks")