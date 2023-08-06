"""
Purger of swarm-bus
"""
import logging

logger = logging.getLogger(__name__)


class Purger(object):
    """
    Purger logic
    """

    def purge_queue(self, queue_name):
        """
        Purge messages into queues
        """
        queue_set = self.get_queue_set(queue_name)

        for queue_priority in queue_set.queues:
            try:
                queue_priority.purge()

                logger.info(
                    "[%s] Queue '%s' is now purged",
                    self.log_namespace,
                    queue_priority.url
                )
            except self.client.exceptions.PurgeQueueInProgress:
                logger.info(
                    "[%s] Queue '%s' is already purged",
                    self.log_namespace,
                    queue_priority.url
                )
