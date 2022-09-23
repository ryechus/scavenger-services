# coding: utf-8
import os.path
from typing import Dict, List  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    File,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    UploadFile,
    status,
)
from fastapi.responses import JSONResponse

from image_service.core.settings import settings
from image_service.lib.storage import delete_image as delete_image_from_storage
from image_service.lib.storage import get_image as get_image_from_storage
from image_service.lib.storage import get_image_url, put_image
from image_service.lib.transform import resize_image
from image_service.models.cache.image import ImageCache
from image_service.models.upload_image201_response import UploadImage201Response

router = APIRouter()


@router.get("/image/{key:path}")
async def get_image(
    key: str = Path(None, description="key of the image to get"),
    width: int = Query(None, description="width of image to return"),
    height: int = Query(None, description="height of image to return"),
    quality: int = Query(100, description="quality of returned image. value should be between 1 and 5"),
):
    if not all([width, height, quality]):
        return f"https://{settings.s3_bucket_name}/{key}"

    filename, ext = os.path.splitext(key)
    thumbnail_key = f"{filename}-{width}x{height}q{quality}{ext}"

    image_cache = ImageCache()

    if thumbnail_key not in image_cache:
        image = await get_image_from_storage(key)
        if not image:
            return JSONResponse(status_code=404, content="image not found")

        r_im = await resize_image(image, width, height, quality)
        await put_image(r_im, thumbnail_key, extra_args={"ContentType": "image/jpeg"})

    return f"https://{settings.s3_bucket_name}/{thumbnail_key}"


@router.delete("/image/{key:path}")
async def delete_image(key: str = Path(...)):
    deleted_image = await delete_image_from_storage(key)

    return deleted_image


@router.post("/upload/")
async def upload_image(file: UploadFile = File(...), key: str = Form(default="")):
    """Upload an image to the service."""
    key = key.strip() if key.strip() else file.filename

    await put_image(file.file, key, extra_args={"ContentType": file.content_type})

    return UploadImage201Response(key=key, url=f"https://{settings.s3_bucket_name}/{key}")
