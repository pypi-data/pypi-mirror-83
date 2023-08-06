# -*- coding: utf-8 -*-

from imio.amqp import BaseConsumer
from imio.amqp import BasePublisher
from imio.amqp import BaseDispatcher
from imio.dataexchange.core.dms import Deliberation
from imio.dataexchange.core.scripts.base import init_dispatcher
from imio.dataexchange.core.scripts.base import init_script


class DeliberationConsumer(BaseConsumer):
    queue = 'dms.deliberation'
    routing_key = 'DELIB'

    def treat_message(self, message):
        self.publisher.publish(message)


class DeliberationPublisher(BasePublisher):
    exchange = 'dms.deliberation'

    def get_routing_key(self, message):
        return message.routing_key

    def transform_message(self, message):
        return Deliberation(message)


class DeliberationDispatcher(BaseDispatcher):
    logger_name = 'deliberation_dispatcher'
    log_file = None


def main():
    config = init_script()
    init_dispatcher(
        config,
        DeliberationDispatcher,
        DeliberationConsumer,
        DeliberationPublisher,
        'DELIB',
    )
