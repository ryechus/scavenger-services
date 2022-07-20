# coding: utf-8

from fastapi.testclient import TestClient

import image_service


def test_get_app_version(client: TestClient):
    """Test case for get_app_version

    Get version
    """

    headers = {}
    response = client.request(
        "GET",
        "/version",
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200
    assert response.json() == image_service.__version__
