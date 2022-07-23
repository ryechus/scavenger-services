import redis

from image_service.core.settings import settings

redis_con = redis.Redis(
    host=settings.redis_host_name, port=settings.redis_host_port, db=0
)
