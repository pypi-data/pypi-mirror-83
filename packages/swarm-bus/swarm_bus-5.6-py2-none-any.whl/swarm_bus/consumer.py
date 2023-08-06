"""
Consumer for swarm-bus
"""
import base64
import datetime
import json
import logging
import time

logger = logging.getLogger(__name__)


class Consumer(object):
    """
    Consumer logic
    """
    polling_messages = 10

    def consume(self, queue_name, callback=None, error_handler=None,
                polling_messages=10, max_messages=100000,
                pre_polling_handler=None, post_polling_handler=None):
        """
        Consume message datas
        """
        self.polling_messages = polling_messages

        try:
            queue_set = self.get_queue_set(queue_name)
        except KeyError:
            raise ValueError(
                "'%s' is an unknown queue" % queue_name
            )

        if callback is None:
            raise ValueError(
                "callback parameter can not be empty"
            )

        callback_wrapped = self.callback_wrapper(callback, error_handler)

        while max_messages > 0:
            if not self.can_consume:
                logger.debug(
                    '[%s] Consuming is on hold. Next try in 60 seconds',
                    self.log_namespace
                )
                sleep_time = 60
            else:
                if pre_polling_handler:
                    pre_polling_handler(max_messages)

                polled = self.polling(
                    queue_set, callback_wrapped,
                    self.polling_messages
                )

                if post_polling_handler:
                    post_polling_handler(max_messages, polled)

                max_messages -= polled

                sleep_time = queue_set.sleep_time
                if sleep_time:
                    logger.debug(
                        '[%s] Sleeping for %s seconds',
                        self.log_namespace,
                        sleep_time
                    )

            time.sleep(sleep_time)

        logger.debug(
            '[%s] Stop consuming messages',
            self.log_namespace
        )

    @property
    def can_consume(self):
        """
        Check a queue can be consumed.
        """
        if not self.transport.office_hours:
            return True

        now = datetime.datetime.now()
        if now.weekday() in [5, 6]:  # Week-end
            return False

        hour = now.hour
        if hour >= 8 and hour < 20:
            return True

        return False

    def polling(self, queue_set, callback_wrapped, polling_messages):
        """
        Poll all the messages availables for each priorities
        """
        total_polled = 0

        for queue_priority in queue_set.queues:
            logger.debug(
                '[%s] Polling %s for %s seconds',
                self.log_namespace,
                queue_priority.url,
                queue_set.polling_interval
            )
            polled_messages = queue_priority.receive_messages(
                WaitTimeSeconds=queue_set.polling_interval,
                MaxNumberOfMessages=polling_messages
            )
            logger.debug(
                '[%s] %s messages polled',
                self.log_namespace,
                len(polled_messages)
            )
            total_polled += len(polled_messages)

            for message in polled_messages:
                body = self.decode_body(message)

                callback_wrapped(
                    body, message
                )

        return total_polled

    def decode_body(self, message):
        """
        Decode the message body for having a dict
        """
        try:
            return json.loads(message.body)
        except ValueError:
            # Old bus compatibility
            return json.loads(
                base64.b64decode(
                    json.loads(
                        base64.b64decode(
                            message.body
                        ).decode('utf8')
                    )['body']
                ).decode('utf8')
            )

    def callback_wrapper(self, callback, error_handler):
        """
        Decorate the callback to log exceptions
        and send them to Senty later if possible.

        Also cancels the exception to avoid process to crash !
        """
        def exception_catcher(body, message):
            """
            Decorator around callback.
            """
            try:
                return callback(body, message)
            except Exception:
                logger.exception(
                    '[%s] Unhandled exception occured !',
                    self.log_namespace
                )
                if error_handler:
                    error_handler(body, message)
                    logger.debug(
                        '[%s] Error handler called',
                        self.log_namespace
                    )

        return exception_catcher
