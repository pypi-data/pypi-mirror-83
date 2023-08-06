from urllib.parse import urlparse

from .base_test_case import BaseTestCase, Producer


class ProducerTestCase(BaseTestCase):
    def test_queue_creation(self):
        queue_name = self.fake.pystr(max_chars=10)
        producer = self.get_producer(queue_name)
        self.assertEqual(producer.queue_name, queue_name)
        url = urlparse(producer.queue.url)
        self.assertEqual(url.path, f"/100010001000/{queue_name}")

    def test_invalid_producer(self):
        self.assertRaises(ValueError, Producer)

    def test_message_publish(self):
        queue_name = self.fake.pystr(max_chars=10)
        producer = self.get_producer(queue_name)
        data = self.fake.json(
            data_columns={
                "name": "company",
                "phrase": "catch_phrase",
                "description": "bs",
                "address": "address",
            }
        )
        return_data = producer.publish(data)
        response_metadata = return_data.get("ResponseMetadata")
        self.assertEqual(response_metadata.get("HTTPStatusCode"), 200)
