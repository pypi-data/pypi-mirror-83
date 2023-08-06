from urllib.parse import urlparse

from .base_test_case import BaseTestCase, ConsumerTest


class ConsumerTestCase(BaseTestCase):
    def test_queue_creation(self):
        queue_name = self.fake.pystr(max_chars=10)
        consumer = self.get_consumer(queue_name)
        self.assertEqual(consumer.queue_name, queue_name)
        url = urlparse(consumer.queue.url)
        self.assertEqual(url.path, f"/100010001000/{queue_name}")

    def test_invalid_consumer(self):
        self.assertRaises(ValueError, ConsumerTest)
