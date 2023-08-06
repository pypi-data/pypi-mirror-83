from unittest import TestCase

from botocore.exceptions import (
    NoCredentialsError,
    NoRegionError,
    EndpointConnectionError,
)

from sqspy import Consumer
from sqspy._base import Base
from .config import TestConfig


class ConnectionTestCase(TestCase):
    def test_endpoint_connection(self):
        base = Base(
            endpoint_url=TestConfig.endpoint_url, region_name=TestConfig.region_name
        )
        self.assertIsNotNone(base)

    def test_connection_error(self):
        self.assertRaises(
            (NoCredentialsError, NoRegionError, EndpointConnectionError),
            Consumer,
            "queue_name",
            region_name=None,
            endpoint_url="http://localhost/",
        )
