import configparser
import sys
import threading
import time
from json import JSONDecodeError

import pika
import logging
import json

from pika.exceptions import ConnectionClosedByBroker, AMQPChannelError, AMQPConnectionError

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)
logging.getLogger('pika').setLevel(logging.WARNING)


class PikaConsumer:
    reconnection_timeout = 5

    def __init__(self, handlers, queue, host, port, user, password, max_length=None, prefetch_count=20):
        self._queue = queue
        self._host = host
        self._port = port
        self._user = user
        self._pass = password
        self._terminate = False
        self._handlers = handlers
        self._connection = None
        self._channel = None
        self._max_length = max_length
        self._disconnection_cs = threading.Lock()
        self._active_callbacks = 0
        self._prefetch_count = prefetch_count
        self._active_threads = []
        # Here we will store messages, which are really processed, but the acknowledge wasn't sent
        self._repeatable_messages = []

    @classmethod
    def create_from_config(cls, handlers, config_path, config_section='consumer'):
        config = configparser.ConfigParser()
        config.readfp(open(config_path))
        queue = config.get(config_section, "queue")
        host = config.get(config_section, "host")
        port = config.get(config_section, "port")
        user = config.get(config_section, "user")
        password = config.get(config_section, "password")
        max_length = config.get(config_section, "max_length", fallback=None)
        return cls(handlers, queue, host, port, user, password, max_length)

    def __del__(self):
        self.terminate()

    def terminate(self):
        self._terminate = True
        self.disconnect()

    def connect(self):
        with self._disconnection_cs:
            logging.info("start connecting on host %s queue %s" % (self._host, self._queue))
            credentials = pika.PlainCredentials(self._user, self._pass)
            parameters = pika.ConnectionParameters(host=self._host, port=self._port, credentials=credentials,
                                                   heartbeat=0)
            self._connection = pika.BlockingConnection(parameters)
            self._channel = self._connection.channel()
            arguments = None
            if self._max_length is not None:
                arguments = {"x-max-length": int(self._max_length), "x-overflow": "reject-publish"}
            self._channel.basic_qos(prefetch_count=self._prefetch_count)
            self._channel.queue_declare(queue=self._queue, durable=True, arguments=arguments)
            self._channel.basic_consume(queue=self._queue, on_message_callback=self._callback)

    def disconnect(self):
        with self._disconnection_cs:
            if self._connection is not None and not self._connection.is_closed:
                logging.info("start server disconnection on host %s queue %s" % (self._host, self._queue))
                try:
                    self._channel.stop_consuming()
                except Exception as ex:
                    logging.error("rabbit stop consuming error: %s" % str(ex),
                                  extra={"queue": self._queue, "host": self._host})
                try:
                    while self._active_callbacks > 0:
                        time.sleep(1)
                    self._connection.close()
                except Exception as ex:
                    logging.error("rabbit disconnect error: %s" % str(ex),
                                  extra={"queue": self._queue, "host": self._host})

    def start(self):
        while not self._terminate:
            try:
                self.connect()
                logging.info("start consuming on host %s queue %s" % (self._host, self._queue))
                self._channel.start_consuming()
            except ConnectionClosedByBroker as ex:
                if not self._terminate:
                    logging.error("server broke the connection: %s in line %s, reconnecting in %d seconds..." %
                                  (str(sys.exc_info()[-1].tb_lineno), str(ex), self.reconnection_timeout),
                                  extra={"queue": self._queue, "host": self._host})
                    time.sleep(self.reconnection_timeout)
            except AMQPChannelError as ex:
                if not self._terminate:
                    logging.error("caught a channel error in line %s: %s, reconnecting..." %
                                  (str(sys.exc_info()[-1].tb_lineno), str(ex)),
                                  extra={"queue": self._queue, "host": self._host})
            except AMQPConnectionError as ex:
                if not self._terminate:
                    logging.error("connection was closed in line %s: %s, reconnecting in %d seconds..." %
                                  (str(sys.exc_info()[-1].tb_lineno), str(ex), self.reconnection_timeout),
                                  extra={"queue": self._queue, "host": self._host})
                    time.sleep(self.reconnection_timeout)
            except Exception as ex:
                if not self._terminate:
                    logging.error("start error in line %s: %s, restart in %d seconds" %
                                  (str(sys.exc_info()[-1].tb_lineno), str(ex), self.reconnection_timeout),
                                  extra={"queue": self._queue, "host": self._host})
                    time.sleep(self.reconnection_timeout)
            finally:
                self.disconnect()
        logging.info("rabbit consumer terminated on host %s queue %s" % (self._host, self._queue))

    def _callback(self, ch, method, properties, body):
        try:
            self._active_callbacks += 1
            message = json.loads(body.decode("utf-8"))
            if "action" in message.keys():
                action = message["action"]
                unique = message["rmq_unique"]
                if action in self._handlers.keys():
                    if unique not in self._repeatable_messages:
                        if self._handlers[action](message):
                            try:
                                ch.basic_ack(delivery_tag=method.delivery_tag)
                            except Exception as ex:
                                logging.error("cannot send acknowledge: %s" % str(ex))
                                self._repeatable_messages.append(unique)
                    else:
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                else:
                    logging.error("no such handler: %s" % action)
            else:
                logging.error("wrong message format: no column action")
        except JSONDecodeError as ex:
            logging.error("json decode error in line %s: %s" % (str(sys.exc_info()[-1].tb_lineno), str(ex)))
        except Exception as ex:
            logging.error("rabbit callback error in line %s: %s" % (str(sys.exc_info()[-1].tb_lineno), str(ex)),
                          extra={"queue": self._queue, "body": body, "host": self._host})
        finally:
            self._active_callbacks -= 1
