import broker
from queue import Queue
import random
import select
import string
import threading
import threatbus
from threatbus.data import Subscription, Unsubscription
from threatbus_zeek.message_mapping import (
    map_to_broker,
    map_to_internal,
    map_management_message,
)
import time

"""Zeek network monitor - plugin for Threat Bus"""

plugin_name = "zeek"
lock = threading.Lock()
subscriptions = dict()


def validate_config(config):
    assert config, "config must not be None"
    config["host"].get(str)
    config["port"].get(int)
    config["module_namespace"].get(str)


def rand_string(length):
    """Generates a pseudo-random string with the requested length"""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def manage_subscription(
    ep, module_namespace, task, subscribe_callback, unsubscribe_callback
):
    global lock, subscriptions
    rand_suffix_length = 10
    if type(task) is Subscription:
        # point-to-point topic and queue for that particular subscription
        logger.info(f"Received subscription for topic: {task.topic}")
        p2p_topic = task.topic + rand_string(rand_suffix_length)
        p2p_q = Queue()
        ack = broker.zeek.Event(
            f"{module_namespace}::subscription_acknowledged", p2p_topic
        )
        ep.publish("threatbus/manage", ack)
        subscribe_callback(task.topic, p2p_q, task.snapshot)
        lock.acquire()
        subscriptions[p2p_topic] = p2p_q
        lock.release()
    elif type(task) is Unsubscription:
        logger.info(f"Received unsubscription from topic: {task.topic}")
        threatbus_topic = task.topic[: len(task.topic) - rand_suffix_length]
        p2p_q = subscriptions.get(task.topic, None)
        if p2p_q:
            unsubscribe_callback(threatbus_topic, p2p_q)
            lock.acquire()
            del subscriptions[task.topic]
            lock.release()
    else:
        logger.debug(f"Skipping unknown management message of type: {type(task)}")


def publish(module_namespace, ep):
    """
    Publishes messages for all subscriptions in a round-robin fashion to via
    broker.
    @param module_namespace A Zeek namespace to use for event sending
    @param ep The broker endpoint used for publishing
    """
    global subscriptions, lock, logger
    while True:
        lock.acquire()
        for topic, q in subscriptions.items():
            if q.empty():
                continue
            msg = q.get()
            if not msg:
                continue
            event = map_to_broker(msg, module_namespace)
            if event:
                ep.publish(topic, event)
                logger.debug(f"Published {msg} on topic {topic}")
            q.task_done()
        lock.release()
        time.sleep(0.05)


def manage(module_namespace, ep, subscribe_callback, unsubscribe_callback):
    """Binds a broker subscriber to the given endpoint. Only listens for
    management messages, such as un/subscriptions of new clients.
    @param module_namespace A Zeek namespace to accept events from
    @param ep The broker endpoint used for listening
    @param subscribe_callback The callback to invoke for new subscriptions
    @param unsubscribe_callback The callback to invoke for revoked subscriptions
    """
    global logger
    sub = ep.make_subscriber("threatbus/manage")
    while True:
        ready = select.select([sub.fd()], [], [])
        if not ready[0]:
            logger.critical("Broker management subscriber filedescriptor error.")
        (topic, broker_data) = sub.get()
        msg = map_management_message(broker_data, module_namespace)
        if msg:
            manage_subscription(
                ep, module_namespace, msg, subscribe_callback, unsubscribe_callback
            )


def listen(module_namespace, ep, inq):
    """Binds a broker subscriber to the given endpoint. Forwards all received
    intel and sightings to the inq.
    @param logger A logging.logger object
    @param module_namespace A Zeek namespace to accept events from
    @param ep The broker endpoint used for listening
    @param inq The queue to forward messages to
    """
    sub = ep.make_subscriber(["threatbus/intel", "threatbus/sighting"])
    global logger
    while True:
        ready = select.select([sub.fd()], [], [])
        if not ready[0]:
            logger.critical("Broker intel/sightings subscriber filedescriptor error.")
        (topic, broker_data) = sub.get()
        msg = map_to_internal(broker_data, module_namespace)
        if msg:
            inq.put(msg)


@threatbus.app
def run(config, logging, inq, subscribe_callback, unsubscribe_callback):
    global logger
    logger = threatbus.logger.setup(logging, __name__)
    config = config[plugin_name]
    try:
        validate_config(config)
    except Exception as e:
        logger.fatal("Invalid config for plugin {}: {}".format(plugin_name, str(e)))
    host, port, namespace = (
        config["host"].get(),
        config["port"].get(),
        config["module_namespace"].get(),
    )
    broker_opts = broker.BrokerOptions()
    broker_opts.forward = False
    ep = broker.Endpoint(broker.Configuration(broker_opts))
    ep.listen(host, port)

    threading.Thread(target=listen, args=(namespace, ep, inq), daemon=True).start()
    threading.Thread(
        target=manage,
        args=(namespace, ep, subscribe_callback, unsubscribe_callback),
        daemon=True,
    ).start()
    threading.Thread(target=publish, args=(namespace, ep), daemon=True).start()
    logger.info("Zeek plugin started")
