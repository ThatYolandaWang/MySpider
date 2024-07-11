import redis
import hashlib

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