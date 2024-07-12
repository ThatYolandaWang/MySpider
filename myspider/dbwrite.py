import redis
import hashlib
import csv

class DBWrite:
    def __init__(self, ip, port, dbnum):
        self.ip = ip
        self.port = port
        self.dbnum = dbnum

    def connect(self):
        redisPool = redis.ConnectionPool(host=self.ip, port=self.port, db=self.dbnum, decode_responses=True)
        self.dbclient = redis.Redis(connection_pool=redisPool)

    def write(self, key, value):
        self.dbclient.set(key, value)

    def close(self):
        self.dbclient.close()

class CSVWrite:
    def __init__(self, file_name) -> None:
        self.file_name = file_name

    def connect(self):
        self.f = open(self.file_name, 'w', encoding='utf-8', newline="")
        self.csv_write = csv.writer(self.f)
        self.csv_write.writerow(['总价', '公寓名', '链接', '地址', '房间数', '面积', '单价', 'ID', '详情', '价格区间'])

    def write(self, key, value):
        self.csv_write.writerow(value)

    def close(self):
        self.f.close()