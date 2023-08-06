"""
Queues for swarm-bus
"""
import logging

logger = logging.getLogger(__name__)


class QueueDoesNotExist(ValueError):
    pass


class Queue(object):
    """
    Queue connector
    """
    def __init__(self, queue_name, transport,
                 polling_interval=None,
                 retention_period=None,
                 visibility_timeout=None,
                 sleep_time=None):

        self.queues = []
        self.queue_name = queue_name
        self.transport = transport

        self.polling_interval = polling_interval or transport.polling_interval
        self.retention_period = retention_period or transport.retention_period
        self.visibility_timeout = visibility_timeout or transport.visibility_timeout  # noqa

        self.sleep_time = sleep_time or transport.sleep_time

    def connect(self, bus):
        """
        Map priorities to Queue with creation if needed
        """
        for priority in self.transport.priorities or ['']:
            name = '%s%s-%s' % (
                self.transport.prefix, self.queue_name, priority
            )
            name = name.strip('-')
            self.queues.append(
                self.get_or_create(name, bus)
            )

    def retrieve(self, bus):
        """
        Map priorities to Queue silently
        """
        for priority in self.transport.priorities or ['']:
            name = '%s%s-%s' % (
                self.transport.prefix, self.queue_name, priority
            )
            name = name.strip('-')
            try:
                self.queues.append(
                    self.get(name, bus)
                )
            except QueueDoesNotExist:
                pass

    def get(self, name, bus):
        """
        Get the queue with priority
        """
        try:
            logger.debug(
                "[%s] Retrieving queue '%s'",
                bus.log_namespace,
                name
            )
            queue = bus.connection.get_queue_by_name(QueueName=name)
        except bus.client.exceptions.QueueDoesNotExist:
            raise QueueDoesNotExist

        return queue

    def get_or_create(self, name, bus):
        """
        Get or create the queue with priority
        """
        try:
            queue = self.get(name, bus)
        except QueueDoesNotExist:
            logger.debug(
                "[%s] Creating queue '%s'",
                bus.log_namespace,
                name
            )
            queue = bus.connection.create_queue(
                QueueName=name,
                Attributes={
                    'VisibilityTimeout': str(self.visibility_timeout),
                    'MessageRetentionPeriod': str(self.retention_period),
                    'ReceiveMessageWaitTimeSeconds': str(self.polling_interval)
                }
            )

        return queue


class QueueManager(object):
    """
    Queue manager
    """

    def declare_queue(self, queue_name, **kwargs):
        """
        Add a queue in the Bus and retrieve URL
        """
        if queue_name in self.queues:
            return self.queues[queue_name]

        queue = Queue(
            queue_name,
            self.transport,
            **kwargs
        )
        self.queues[queue_name] = queue

        queue.retrieve(self)

        return queue

    def register_queue(self, queue_name, **kwargs):
        """
        Add a queue in the Bus and create or retrieve URL
        """
        if queue_name in self.queues:
            return self.queues[queue_name]

        queue = Queue(
            queue_name,
            self.transport,
            **kwargs
        )
        self.queues[queue_name] = queue

        queue.connect(self)

        return queue

    def get_queue_set(self, queue_name):
        """
        Return the set of queue
        """
        if queue_name not in self.queues:
            raise ValueError(
                "'%s' is an unknown queue" % queue_name
            )

        return self.queues[queue_name]

    def get_queue(self, queue_name, priority=0):
        """
        Return the queue binded to a priority
        """
        queues = self.get_queue_set(queue_name).queues

        return queues[priority]
