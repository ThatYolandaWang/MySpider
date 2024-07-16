import redis
import os
import csv


class DBWrite:
    def __init__(self, ip, port, dbnum):
        self.ip = ip
        self.port = port
        self.dbnum = dbnum

    def open(self):
        redisPool = redis.ConnectionPool(host=self.ip, port=self.port, db=self.dbnum, decode_responses=True)
        self.dbclient = redis.Redis(connection_pool=redisPool)

    def write(self, key, value):
        self.dbclient.set(key, value)


    def close(self):
        self.dbclient.close()


class CSVWrite:
    def __init__(self, filename):
        self.filename = os.path.abspath(os.path.dirname(__file__)) + '\\..\\' + filename

    def open(self):
        self.f = open(self.filename, 'w', encoding='utf-8', newline='')
        headers = ['id', 'name', 'price', 'room', 'size', 'unit', 'floor', 'address', 'linkage', 'createdAt', 'modifiedAt', 'Build_year', 'Building_floors_num', 'Building_ownership', 'Building_type', 'Construction_status', 'Energy_certificate', 'Rent', 'hidePrice', 'lat', 'long', 'lowerPredictionPrice', 'lowerPredictionPricePerM', 'predictionPrice', 'upperPredictionPrice', 'upperPredictionPricePerM']
        self.writer = csv.DictWriter(self.f, headers)
        self.writer.writeheader()

    def write(self, line):
        self.writer.writerow(line)
    
    def close(self):
        self.f.close()