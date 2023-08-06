"""
Swarm Bus
"""
from swarm_bus.connector import BusConnector
from swarm_bus.connector import BusContextManager
from swarm_bus.consumer import Consumer
from swarm_bus.deleter import Deleter
from swarm_bus.lister import Lister
from swarm_bus.publisher import Publisher
from swarm_bus.purger import Purger
from swarm_bus.queue import QueueManager


class SwarmBus(
        BusConnector,
        BusContextManager,
        QueueManager,
        Deleter,
        Lister,
        Purger,
        Publisher,
        Consumer
):
    pass
