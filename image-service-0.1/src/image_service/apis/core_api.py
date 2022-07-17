# coding: utf-8
import os.path
from typing import Dict, List  # noqa: F401

import boto3
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

from image_service.lib.storage import get_image as get_image_from_storage
from image_service.lib.storage import get_image_url, put_image
from image_service.lib.transform import resize_image

router = APIRouter()


@router.get("/image/{key}")
async def get_image(
    key: str = Path(None, description="key of the image to get"),
    width: int = Query(None, description="width of image to return"),
    height: int = Query(None, description="height of image to return"),
    quality: int = Query(100, description="quality of returned image. value should be between 1 and 5"),
):
    file = get_image_from_storage(key)

    r_im = await resize_image(file, width, height, quality)

    filename, ext = os.path.splitext(key)
    thumbnail_key = f"{filename}-{width}x{height}q{quality}{ext}"

    response = get_image_url(thumbnail_key)

    await put_image(r_im, thumbnail_key, extra_args={"ContentType": "image/jpeg"})

    return response


@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    """Upload an image to the service."""
    session = boto3.Session(profile_name="hohomike", region_name="us-west-1")
    s3 = session.client("s3")

    s3.upload_fileobj(
        file.file, "scavenger-image-service", file.filename, ExtraArgs={"ContentType": file.content_type}
    )
    return {"filename": file.filename}
