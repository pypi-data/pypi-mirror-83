from json import loads

from .base_test_case import BaseTestCase


class ProducerTestCase(BaseTestCase):
    def test_message_acknowledgement(self):
        queue_name = self.fake.pystr(max_chars=10)
        producer = self.get_producer(queue_name)
        consumer = self.get_consumer(queue_name, max_number_of_messages=1)
        message = self.fake.json(
            data_columns={
                "name": "company",
                "phrase": "catch_phrase",
                "description": "bs",
                "address": "address",
            }
        )
        message_data = producer.publish(message)
        fetched_message = consumer.poll_messages()[0]
        self.assertEqual(
            fetched_message.md5_of_body, message_data.get("MD5OfMessageBody")
        )
        self.assertEqual(fetched_message.message_id, message_data.get("MessageId"))
        self.assertEqual(message, loads(fetched_message.body))
