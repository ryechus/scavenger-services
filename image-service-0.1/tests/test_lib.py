import boto3
import pytest
from moto import mock_s3

from image_service.core.settings import settings
from image_service.lib.storage import get_image, put_image
from image_service.lib.transform import resize_image


@pytest.fixture
def boto3_session():
    with mock_s3():
        session = boto3.Session()
        yield session


@pytest.fixture
def s3_client(boto3_session):
    yield boto3_session.client("s3")


@pytest.fixture
def s3_bucket(s3_client):
    s3_client.create_bucket(Bucket=settings.s3_bucket_name)

    yield


@pytest.fixture
def s3_object(s3_client, s3_bucket):
    s3_client.put_object(
        Body=b"this is a test string", Bucket=settings.s3_bucket_name, Key="test"
    )

    yield


def test_get_image(s3_object):
    file = get_image("test")

    assert hasattr(file, "read")
    assert hasattr(file, "seek")
    assert hasattr(file, "tell")


def test_get_image_not_found(s3_bucket):
    file = get_image("test")

    assert file is None


@pytest.mark.parametrize("width,height", [("100", "100"), (100, 100)])
@pytest.mark.asyncio
async def test_resize_image(s3_client, s3_bucket, width, height, local_image):
    file = local_image

    r_im = await resize_image(file, width, height)

    await put_image(r_im, "test_thumbnail", extra_args={"ContentType": "image/jpeg"})

    new_image = get_image("test_thumbnail")

    assert hasattr(new_image, "read")
    assert hasattr(new_image, "seek")
    assert hasattr(new_image, "tell")
