# coding: utf-8

from typing import Dict, List  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

import image_service
from image_service.models.error import Error
from image_service.models.extra_models import TokenModel  # noqa: F401

router = APIRouter()


@router.get(
    "/version",
    responses={
        200: {"model": str, "description": "success"},
        500: {"model": Error, "description": "server error"},
    },
    tags=["diagnostic"],
    summary="Get version",
    response_model_by_alias=True,
)
async def get_app_version() -> str:
    """Application version for the service"""
    return image_service.__version__
