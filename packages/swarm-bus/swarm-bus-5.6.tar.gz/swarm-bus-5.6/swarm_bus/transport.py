"""
Connector for swarm-bus
"""
import logging
import os
import socket

from swarm_bus.constants import OFFICE_HOURS
from swarm_bus.constants import POLLING_INTERVAL
from swarm_bus.constants import PREFIX
from swarm_bus.constants import PRIORITIES
from swarm_bus.constants import REGION
from swarm_bus.constants import RETENTION_PERIOD
from swarm_bus.constants import SLEEP_TIME
from swarm_bus.constants import VISIBILITY_TIMEOUT


logger = logging.getLogger(__name__)


class Transport(object):
    """
    Default transport configuration for SQS
    """
    def __init__(self,
                 access_key,
                 secret_key,
                 prefix=PREFIX,
                 priorities=PRIORITIES,
                 polling_interval=POLLING_INTERVAL,
                 retention_period=RETENTION_PERIOD,
                 visibility_timeout=VISIBILITY_TIMEOUT,
                 sleep_time=SLEEP_TIME,
                 office_hours=OFFICE_HOURS,
                 region=REGION):
        # S3
        self.access_key = access_key
        self.secret_key = secret_key

        # SQS
        self.region = region
        self.prefix = prefix % {
            'hostname': self.get_hostname()
        }

        # Priorities
        self.priorities = priorities

        # Offfice hours
        self.office_hours = office_hours

        # Queue default config
        self.polling_interval = polling_interval
        self.retention_period = retention_period
        self.visibility_timeout = visibility_timeout
        self.sleep_time = sleep_time

    def get_hostname(self):
        """
        Method for having consistent hostname accross hosts.
        """
        default = socket.gethostname()
        hostname = os.getenv('AMQP_HOSTNAME', default)

        return hostname
