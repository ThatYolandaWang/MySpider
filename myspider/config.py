import configparser,json, os
import platform

class config:
    def __init__(self):
        cfg_path = ""
        sysstr = platform.system()
        if(sysstr =="Windows"):
            cfg_path = os.path.dirname(os.path.realpath(__file__))+'\\config.ini'
        else:
            cfg_path = os.path.dirname(os.path.realpath(__file__))+'/config.ini'

        print('config.ini path:', cfg_path)
        self.cfg = configparser.ConfigParser()
        self.cfg.read(cfg_path, encoding='utf-8-sig')

    def get_db_ip(self):
        return self.cfg.get('db','IP')
    
    def get_db_port(self):
        return self.cfg.getint('db', 'port')
    
    def get_db_num(self):
        return self.cfg.getint('db', 'dbnum')

    def get_url_list(self):
        base_url = self.cfg.get('spider','url')
        site_list = json.loads(self.cfg.get('spider','cityls'))
        url_list = []
        i = 0
        for site in site_list:
            url = base_url +"/"+site+"?viewType=listing"
            url_list.insert(i, url)
            i+=1

        if len(site_list)==0:
            url_list.insert(0, base_url)

        return url_list
    
    def get_test_status(self):
        return (self.cfg.getint('debug', 'test')==1)