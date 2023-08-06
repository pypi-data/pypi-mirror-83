# encoding: utf-8

from imio.amqp import BaseConsumer
from imio.amqp import BasePublisher
from imio.amqp import BaseDispatcher
from imio.dataexchange.core.dms import IncomingMail
from imio.dataexchange.core.scripts.base import init_dispatcher
from imio.dataexchange.core.scripts.base import init_script


class IncomingMailConsumer(BaseConsumer):
    queue = 'dms.incomingmail'
    routing_key = 'COUR_E'

    def treat_message(self, message):
        self.publisher.publish(message)


class IncomingMailPublisher(BasePublisher):
    exchange = 'dms.incomingmail'

    def get_routing_key(self, message):
        return message.routing_key

    def transform_message(self, message):
        return IncomingMail(message)


class IncomingMailDispatcher(BaseDispatcher):
    logger_name = 'incomingmail_dispatcher'
    log_file = None


def main():
    config = init_script()
    init_dispatcher(config, IncomingMailDispatcher, IncomingMailConsumer,
                    IncomingMailPublisher, 'COUR_E')
