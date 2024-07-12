import configparser,json, os


class config:
    def __init__(self):
        cfg_path = os.path.dirname(os.path.realpath(__file__))+'\\config.ini'
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
            url = base_url +site+"?viewType=listing"
            url_list.insert(i, url)
            i+=1
        return url_list