import logging.config

from image_service.core.settings import settings


LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"default": {"format": "[%(asctime)s: %(levelname)s/%(name)s]: %(message)s"}},
    "handlers": {"default": {"class": "logging.StreamHandler", "formatter": "default"}},
    "loggers": {"image-service": {"level": settings.log_level, "handlers": ["default"], "propagate": False}},
}

logging.config.dictConfig(LOG_CONFIG)

logger = logging.getLogger("image-service")
