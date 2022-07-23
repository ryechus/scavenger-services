from image_service.core.settings import settings
from image_service.lib.redis import silent_connection
from image_service.models.cache.base import Cache


class ImageCache(Cache):
    @silent_connection
    def __contains__(self, key):
        return self.conn.sismember(settings.image_key_name, key)

    @silent_connection
    def add(self, value):
        _ = self.conn.sadd(settings.image_key_name, value)
