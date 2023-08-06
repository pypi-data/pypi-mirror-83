# encoding: utf-8

from ConfigParser import ConfigParser
from imio.dataexchange.db import DBSession
from imio.dataexchange.db import DeclarativeBase
from imio.dataexchange.db.mappers.file import File
from pika.exceptions import AMQPConnectionError
from sqlalchemy import distinct
from sqlalchemy import engine_from_config

import argparse
import time


def init_script():
    parser = argparse.ArgumentParser(description=u"Initialize the database")
    parser.add_argument("config_uri", type=str)

    args = parser.parse_args()
    config = ConfigParser()
    config.read(args.config_uri)

    init_database(config._sections.get("app:main"))

    return config


def init_database(config):
    engine = engine_from_config(config, prefix="sqlalchemy.")
    # Remove the transaction manager
    del DBSession.session_factory.kw["extension"]
    DBSession.configure(bind=engine)
    DeclarativeBase.metadata.bind = engine


def get_client_ids(file_type):
    query = DBSession.query(distinct(File.client_id))
    query = query.filter(File.type == file_type)
    return [l[0] for l in query.all()]


def generate_dispatcher(dispatcher_cls, consumer_cls, publisher_cls, url):
    params = "connection_attempts=3&heartbeat_interval=3600"
    dispatcher = dispatcher_cls(
        consumer_cls, publisher_cls, "{0}/%2Fwebservice?{1}".format(url, params)
    )
    return dispatcher


def init_dispatcher(config, dispatcher_cls, consumer_cls, publisher_cls, file_type):
    amqp_url = config.get("app:main", "rabbitmq.url")
    client_ids = get_client_ids(file_type)
    wait = 0
    while not client_ids:
        wait += 1
        sleep_duration = wait * 60
        if sleep_duration > 360:
            sleep_duration = 360
        print("There is no message to publish for type ({0})".format(file_type))
        time.sleep(sleep_duration)
        client_ids = get_client_ids(file_type)
    while True:
        try:
            dispatcher = generate_dispatcher(
                dispatcher_cls, consumer_cls, publisher_cls, amqp_url
            )
            for client_id in client_ids:
                queue_name = "{0}.{1}".format(consumer_cls.queue, client_id)
                dispatcher.publisher.setup_queue(queue_name, client_id)
            dispatcher.start()
        except AMQPConnectionError:
            if getattr(dispatcher, "_connection", False):
                try:
                    dispatcher.stop()
                except AttributeError:
                    # This error happen when RabbitMQ is not ready yet
                    pass
            time.sleep(1)
        except KeyboardInterrupt:
            dispatcher.stop()
            break
