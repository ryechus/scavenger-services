import boto3
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from moto import mock_s3

from image_service.core.settings import settings
from image_service.main import app as application


@pytest.fixture
def app() -> FastAPI:
    application.dependency_overrides = {}

    return application


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)


@pytest.fixture
def boto3_session():
    with mock_s3():
        session = boto3.Session(
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
        yield session


@pytest.fixture
def s3_client(boto3_session):
    yield boto3_session.client("s3")
