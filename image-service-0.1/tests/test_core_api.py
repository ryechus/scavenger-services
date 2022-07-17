# coding: utf-8

from fastapi.testclient import TestClient


from image_service.models.error import Error  # noqa: F401
from image_service.models.upload_image201_response import UploadImage201Response  # noqa: F401
from image_service.models.upload_image_request import UploadImageRequest  # noqa: F401


def test_get_image(client: TestClient):
    """Test case for get_image

    Get Image
    """
    params = [("width", {"width":500}),     ("height", {"height":500}),     ("quality", {"quality":3})]
    headers = {
    }
    response = client.request(
        "GET",
        "/image/{key}".format(key='[\"example.jpg\"]'),
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_upload_image(client: TestClient):
    """Test case for upload_image

    Upload Image
    """
    upload_image_request = image_service.UploadImageRequest()

    headers = {
    }
    response = client.request(
        "POST",
        "/upload",
        headers=headers,
        json=upload_image_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

