# -*- coding: utf-8 -*-

from imio.amqp import BaseConsumer
from imio.amqp import BasePublisher
from imio.amqp import BaseDispatcher
from imio.dataexchange.core.dms import IncomingEmail
from imio.dataexchange.core.scripts.base import init_dispatcher
from imio.dataexchange.core.scripts.base import init_script


class IncomingEmailConsumer(BaseConsumer):
    queue = 'dms.incoming.email'
    routing_key = 'EMAIL_E'

    def treat_message(self, message):
        self.publisher.publish(message)


class IncomingEmailPublisher(BasePublisher):
    exchange = 'dms.incoming.email'

    def get_routing_key(self, message):
        return message.routing_key

    def transform_message(self, message):
        return IncomingEmail(message)


class IncomingEmailDispatcher(BaseDispatcher):
    logger_name = 'incoming_email_dispatcher'
    log_file = None


def main():
    config = init_script()
    init_dispatcher(
        config,
        IncomingEmailDispatcher,
        IncomingEmailConsumer,
        IncomingEmailPublisher,
        'EMAIL_E',
    )
