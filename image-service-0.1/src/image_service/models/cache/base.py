from image_service.core.connections import redis_con
from image_service.lib.redis import silent_connection


class Cache:
    def __init__(self, expires_in=30):
        self.conn = redis_con
        self.expires_in = expires_in

    @silent_connection
    def set(self, key, value):
        self.conn.set(key, value, self.expires_in)

    @silent_connection
    def get(self, key):
        return self.conn.get(key)
