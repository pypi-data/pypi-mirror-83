"""
Deleter of swarm-bus
"""
import logging

logger = logging.getLogger(__name__)


class Deleter(object):
    """
    Deleter logic
    """

    def delete_queue(self, queue_name):
        """
        Delete queue
        """
        queue_set = self.get_queue_set(queue_name)

        for queue_priority in queue_set.queues:
            queue_priority.delete()

            logger.info(
                "[%s] Queue '%s' is now deleted",
                self.log_namespace,
                queue_priority.url
            )
