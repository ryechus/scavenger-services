import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from image_service.main import app as application


@pytest.fixture
def app() -> FastAPI:
    application.dependency_overrides = {}

    return application


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)


@pytest.fixture
def local_image():
    file = open(os.path.join(os.path.dirname(__file__), "assets/wrdsmth.JPG"), "rb")

    yield file

    file.close()
