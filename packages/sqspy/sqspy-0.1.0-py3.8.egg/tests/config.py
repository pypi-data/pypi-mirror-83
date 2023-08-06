from os import getenv


class TestConfig:
    aws_access_key_id: str = "XXXXXXXXXXXXXXXX"
    aws_secret_access_key: str = "XXXXXXXXXXXXXXXXXXXXXXXXXX"
    endpoint_url: str = getenv("ENDPOINT_URL")
    region_name: str = getenv("AWS_DEFAULT_REGION") or getenv("REGION_NAME")
