import json
import os
from typing import Dict

import pika

from bwi._internal_logging import BwiLogger

INTERNAL_VHOST = "internals"
RABBIT_HOST = os.environ.get('BWI_RABBIT_HOSTNAME')
RABBIT_VHOST = os.environ.get('RABBIT_VHOST')
RABBIT_USERID = os.environ.get('BWI_RABBIT_USER')
RABBIT_PASSWORD = os.environ.get('BWI_RABBIT_PASSWORD')
RABBIT_CREDENTIALS = pika.PlainCredentials(RABBIT_USERID, RABBIT_PASSWORD)
_rabbit_channel = None


class RabbitMQConnection:
    """
    Used for sending message inside a BWI RabbitMQ server
    """

    class __RabbitMQConnection:
        """
        Singleton to have only one connection per vhost for a worker
        """
        rabbit_channel = None
        internal_broker_chan = None

        def get_channel(self, virtual_host):
            """
            Get a RabbitMQ channel from a given virtual host

            :param virtual_host: vhost name
            :return: a RabbitMQ channel
            """
            rabbit_connection = pika.BlockingConnection(
                pika.ConnectionParameters(heartbeat=65535,
                                          blocked_connection_timeout=65535,
                                          host=RABBIT_HOST,
                                          credentials=RABBIT_CREDENTIALS,
                                          virtual_host=virtual_host))
            return rabbit_connection.channel()

        def __init__(self):
            self.rabbit_channel = self.get_channel(RABBIT_VHOST)
            self.internal_broker_chan = self.get_channel(INTERNAL_VHOST)

    instance = None

    def __init__(self):
        if not RabbitMQConnection.instance:
            RabbitMQConnection.instance = \
                RabbitMQConnection.__RabbitMQConnection()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def send_to_queue(self, queue_name: str, message: Dict):
        """
        Send a message to the project virtual host, mainly for metrics

        :param queue_name: queue name in which we want to send a message
        :param message: message to send
        """
        jsonified = json.dumps(message)
        self.rabbit_channel.basic_publish(exchange='',
                                          routing_key=queue_name,
                                          body=jsonified)
        BwiLogger().logger.info('Sent message "' + jsonified + '" to queue "' + queue_name + '"')

    def send_to_internal_queue(self, queue_name: str, message: Dict):
        """
        Send a message to the internals virtual host, mainly for logs

        :param queue_name: queue name in which we want to send a message
        :param message: message to send
        """
        jsonified = json.dumps(message)
        self.internal_broker_chan.basic_publish(exchange='',
                                                routing_key=queue_name,
                                                body=jsonified)
        BwiLogger().logger.info('Sent message "' + jsonified + '" to internal queue "' + queue_name + '"')
