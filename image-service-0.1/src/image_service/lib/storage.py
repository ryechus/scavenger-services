import boto3
from botocore.exceptions import ClientError

from image_service.core.logging import logger
from image_service.core.settings import settings
from image_service.models.cache.image import ImageCache

s3 = boto3.client("s3")


async def does_image_exist(key):
    try:
        s3.get_object_attributes(
            Bucket=settings.s3_bucket_name,
            Key=key,
            ObjectAttributes=[
                "Checksum",
            ],
        )
    except ClientError:
        #  get_object_attributes will only raise a ClientError if the key doesn't exist
        return False

    return True


async def get_image(key):
    """Returns a file-like object for an image managed by the service"""
    try:
        s3_file = s3.get_object(Bucket=settings.s3_bucket_name, Key=key)
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "NoSuchKey":
            logger.debug("No object found - returning empty")
            return
        else:
            raise exc

    return s3_file["Body"]


async def put_image(file, key, extra_args=None):
    """Uploads an image to the storage backend"""
    s3.upload_fileobj(file, settings.s3_bucket_name, key, ExtraArgs=extra_args)

    s3_file = s3.get_object(Bucket=settings.s3_bucket_name, Key=key)

    image_cache = ImageCache()
    image_cache.add(key)

    return s3_file["Body"]


def get_image_url(key, expires_in=30):
    """Get URL for image in storage in backend

    This is a pre-signed URL that expires after 30 seconds -- this amount of time will probably
    """
    image_cache = ImageCache(expires_in=expires_in)
    presigned_url = image_cache.get(key)

    if not presigned_url:
        response = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.s3_bucket_name, "Key": key},
            ExpiresIn=expires_in,
        )
        # redis_con.set(key, response, expires_in)
        image_cache.set(key, response)
        presigned_url = response

    return presigned_url
