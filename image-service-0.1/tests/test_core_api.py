# coding: utf-8
import os
from urllib.parse import urlparse

import boto3
import pytest
import pytest_asyncio
from botocore.exceptions import ClientError

from image_service.core.settings import settings
from image_service.lib.storage import put_image
from image_service.models.error import Error  # noqa: F401

pytestmark = pytest.mark.aws


@pytest.fixture(scope="session", autouse=True)
def s3_bucket():
    s3_resource = boto3.resource("s3")

    if not settings.s3_bucket_name.endswith(".test"):
        raise pytest.fail("Must use an S3 bucket name that ends in .test")

    try:
        bucket = s3_resource.create_bucket(Bucket=settings.s3_bucket_name)
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
            bucket = s3_resource.Bucket(settings.s3_bucket_name)
        else:
            raise exc

    yield bucket

    bucket.objects.all().delete()


@pytest_asyncio.fixture
async def s3_object(local_image):
    file = local_image
    filename = os.path.split(file.name)[-1]
    image = await put_image(file, filename)

    yield image

    s3_client = boto3.client("s3")

    s3_client.delete_object(Bucket=settings.s3_bucket_name, Key=filename)

    file.close()


@pytest.mark.asyncio
async def test_get_image(client, s3_object):
    """Test case for getting an image from the storage backend"""
    width, height, quality = [10, 10, 10]
    headers = {}
    response = client.request(
        "GET",
        "/image/wrdsmth.JPG",
        headers=headers,
        params={"width": width, "height": height, "quality": quality},
    )

    assert response.status_code == 200
    assert (
        os.path.split(urlparse(response.json()).path)[-1]
        == f"wrdsmth-{width}x{height}q{quality}.JPG"
    )


def test_get_image_not_found(client):
    """Test case for getting an image from the storage backend"""
    headers = {}
    response = client.request(
        "GET",
        "/image/test",
        headers=headers,
        params={"width": "10", "height": "10", "quality": "3"},
    )

    assert response.status_code == 404


def test_upload_image(client, local_image):
    """Test case for upload_image

    Upload Image
    """
    file = local_image
    headers = {}
    response = client.request("POST", "/upload/", headers=headers, files={"file": file})

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200
    assert response.json()["filename"] == "wrdsmth.JPG"
