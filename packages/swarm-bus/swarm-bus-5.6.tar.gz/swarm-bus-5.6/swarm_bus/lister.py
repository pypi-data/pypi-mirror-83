"""
Lister of swarm-bus
"""
import logging

logger = logging.getLogger(__name__)


class Lister(object):
    """
    Lister logic
    """

    def list_queues(self, prefix=''):
        """
        List registered queues
        """
        queues = []
        queue_prefix = self.transport.prefix + prefix

        for queue in self.client.list_queues(
                QueueNamePrefix=queue_prefix).get('QueueUrls', []):
            queues.append(queue)

        return queues

    def list_queues_detail(self):
        """
        List registered queues in detail
        """
        queues = {}

        logger.info(
            "[%s] Getting details for all queues",
            self.log_namespace
        )
        for queue in self.list_queues():
            try:
                response = self.client.get_queue_attributes(
                    QueueUrl=queue,
                    AttributeNames=['All']
                )
                queues[queue] = response['Attributes']
            except self.client.exceptions.QueueDoesNotExist:
                pass

        return queues
