# encoding: utf-8

from imio.amqp import BaseConsumer
from imio.amqp import BasePublisher
from imio.amqp import BaseDispatcher
from imio.dataexchange.core.dms import OutgoingMail
from imio.dataexchange.core.scripts.base import init_dispatcher
from imio.dataexchange.core.scripts.base import init_script


class OutgoingMailConsumer(BaseConsumer):
    queue = 'dms.outgoingmail'
    routing_key = 'COUR_S'

    def treat_message(self, message):
        self.publisher.publish(message)


class OutgoingMailPublisher(BasePublisher):
    exchange = 'dms.outgoingmail'

    def get_routing_key(self, message):
        return message.routing_key

    def transform_message(self, message):
        return OutgoingMail(message)


class OutgoingMailDispatcher(BaseDispatcher):
    logger_name = 'outgoingmail_dispatcher'
    log_file = None


def main():
    config = init_script()
    init_dispatcher(config, OutgoingMailDispatcher, OutgoingMailConsumer,
                    OutgoingMailPublisher, 'COUR_S')
