from pydantic import BaseSettings


class APISettings(BaseSettings):
    log_level: str = "INFO"
    s3_bucket_name: str = "scavenger-image-service"


class AWSSettings(BaseSettings):
    class Config:
        env_file = "aws.env"

    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_default_region: str = "us-west-1"


class ProjectSettings(APISettings, AWSSettings):
    image_key_name: str = "images"


settings = ProjectSettings()
