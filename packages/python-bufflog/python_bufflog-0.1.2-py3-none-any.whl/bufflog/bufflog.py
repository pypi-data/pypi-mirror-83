import structlog
import logging
import sys

from structlog.processors import JSONRenderer
from structlog.stdlib import filter_by_level
from structlog.stdlib import add_log_level_number


def rename_message_key(_, __, event_dict):
    event_dict["message"] = event_dict["event"]
    event_dict.pop("event", None)
    return event_dict


def increase_level_numbers(_, __, event_dict):
    event_dict["level"] = event_dict["level_number"] * 10
    event_dict.pop("level_number", None)
    return event_dict


def get_logger(name=__name__):

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    processors = [
        filter_by_level,
        rename_message_key,
        add_log_level_number,
        increase_level_numbers,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        JSONRenderer(),
    ]
    structlog.configure(
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
        processors=processors,
    )
    return structlog.get_logger(name).new()
