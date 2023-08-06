"""
Connector for swarm-bus
"""
import logging

import boto3

from swarm_bus.transport import Transport

logger = logging.getLogger(__name__)


class BusConnector(object):
    """
    Bus connector logic
    """
    log_namespace = 'Swarm-Bus'
    connection = None
    client = None

    def __init__(self, **transport):
        """
        Handle transport and connection
        """
        self.queues = {}
        self.transport = Transport(**transport)

    def connect(self):
        """
        Connect to SQS resource
        """
        session = boto3.session.Session(
            aws_access_key_id=self.transport.access_key,
            aws_secret_access_key=self.transport.secret_key,
            region_name=self.transport.region
        )

        self.connection = session.resource('sqs', use_ssl=True)
        self.client = self.connection.meta.client

        logger.debug(
            "[%s] Connected to SQS, using '%s' prefix",
            self.log_namespace,
            self.transport.prefix
        )

    def disconnect(self):
        """
        Disconnect to SQS resource
        """
        if self.connection:
            self.queues = {}
            self.client = None
            self.connection = None
            logger.debug(
                '[%s] Disconnected from SQS',
                self.log_namespace
            )


class BusContextManager(object):
    """
    Context Manager features for AMQP.
    """
    def __del__(self):
        """
        Close the connection when garbage collected.
        """
        self.disconnect()

    def __enter__(self):
        """
        Context manager establishing connection.
        """
        if self.connection is None:
            self.connect()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """
        Context manager closing connection.
        """
        self.disconnect()
