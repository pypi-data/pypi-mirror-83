from unittest import TestCase
from faker import Faker
from sqspy import Consumer, Producer
from .config import TestConfig


class ConsumerTest(Consumer):
    def handle_message(self, body, attributes, messages_attributes):
        return body, attributes, messages_attributes


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.fake = Faker()

    @staticmethod
    def get_producer(queue_name, *args, **kwargs):
        return Producer(
            queue_name,
            aws_access_key_id=TestConfig.aws_access_key_id,
            aws_secret_access_key=TestConfig.aws_secret_access_key,
            endpoint_url=TestConfig.endpoint_url,
            region_name=TestConfig.region_name,
            *args,
            **kwargs,
        )

    @staticmethod
    def get_consumer(queue_name, *args, **kwargs):
        return ConsumerTest(
            queue_name,
            aws_access_key_id=TestConfig.aws_access_key_id,
            aws_secret_access_key=TestConfig.aws_secret_access_key,
            endpoint_url=TestConfig.endpoint_url,
            region_name=TestConfig.region_name,
            *args,
            **kwargs,
        )
