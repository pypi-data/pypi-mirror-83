import os
from datetime import datetime
from bwi._queue_sender import RabbitMQConnection
from bwi._internal_logging import BwiLogger


def _generate_message(metric_type: str, name: str, val: float):
    current_timestamp = datetime.timestamp(datetime.now())
    RabbitMQConnection().send_to_queue(
        queue_name="metrics",
        message={'type': metric_type, 'metric_name': name, 'value': val, 'timestamp': current_timestamp})
    return "Message sended"


def store(metric_name: str, value: float):
    """
    For a given metric, store a value inside Graphite.

    We send this value to a dedicated queue, which will do the saving in
    graphite

    We store the value if we are on the BWI Infra, else, we display it.
    :param metric_name: the name of the metric
    :param value: the value of the current action
    """
    if os.environ.get('BWI_INFRA') is not None:
        _generate_message('value', metric_name, value)
    else:
        BwiLogger().logger.info(metric_name, value)


def counter(metric_name: str, value: float):
    """
    For a given metric, increment a counter inside Graphite.

    We send this value to a dedicated queue, which will do the saving in
    graphite

    We store the value if we are on the BWI Infra, else, we display it.
    :param metric_name: the name of the metric
    :param value: the value of the current action
    """
    if os.environ.get('BWI_INFRA') is not None:
        _generate_message('counter', metric_name, value)
    else:
        BwiLogger().logger.info(metric_name, value)
