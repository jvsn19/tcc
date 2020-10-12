import redis

class RedisClient:
    def __init__(self, db = 0):
        '''
        Init the RedisClient instance. It should be the direct contact with the redis-server on this machine.
        '''
        self.db = db
        self.redis = redis.Redis()

    def ping(self) -> bool:
        try:
            return self.redis.ping()
        except redis.exceptions.ConnectionError as ex:
            return False

    def set(self, key, value, expiration = None) -> bool:
        self.redis.set(name = key, value= value)

    def get(self, key) -> bool:
        self.redis.get(name = key)

    def flushall(self) -> bool:
        self.redis.flushall()

    def flushdb(self) -> bool:
        self.redis.flushdb
