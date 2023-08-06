# -*- coding: utf-8 -*-

from imio.amqp import BaseConsumer
from imio.amqp import BasePublisher
from imio.amqp import BaseDispatcher
from imio.dataexchange.core.dms import OutgoingGeneratedMail
from imio.dataexchange.core.scripts.base import init_dispatcher
from imio.dataexchange.core.scripts.base import init_script


class OutgoingGeneratedMailConsumer(BaseConsumer):
    queue = 'dms.outgoinggeneratedmail'
    routing_key = 'COUR_S_GEN'

    def treat_message(self, message):
        self.publisher.publish(message)


class OutgoingGeneratedMailPublisher(BasePublisher):
    exchange = 'dms.outgoinggeneratedmail'

    def get_routing_key(self, message):
        return message.routing_key

    def transform_message(self, message):
        return OutgoingGeneratedMail(message)


class OutgoingGeneratedMailDispatcher(BaseDispatcher):
    logger_name = 'outgoinggeneratedmail_dispatcher'
    log_file = None


def main():
    config = init_script()
    init_dispatcher(
        config,
        OutgoingGeneratedMailDispatcher,
        OutgoingGeneratedMailConsumer,
        OutgoingGeneratedMailPublisher,
        'COUR_S_GEN',
    )
