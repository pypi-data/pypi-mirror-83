import structlog
import logging
import os
import sys

# try:
#     import ddtrace
#     from ddtrace.helpers import get_correlation_ids

#     ddtrace_available = True
# except ImportError:
#     ddtrace_available = False

from structlog.processors import JSONRenderer
from structlog.stdlib import filter_by_level
from structlog.stdlib import add_log_level_number

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# def tracer_injection(logger, log_method, event_dict):
#     # get correlation ids from current tracer context
#     trace_id, span_id = get_correlation_ids()

#     # add ids to structlog event dictionary
#     event_dict["dd.trace_id"] = trace_id or 0
#     event_dict["dd.span_id"] = span_id or 0

#     # add the env, service, and version configured for the tracer
#     event_dict["dd.env"] = ddtrace.config.env or ""
#     event_dict["dd.service"] = ddtrace.config.service or ""
#     event_dict["dd.version"] = ddtrace.config.version or ""

#     return event_dict


def rename_message_key(_, __, event_dict):
    event_dict["message"] = event_dict["event"]
    event_dict.pop("event", None)
    return event_dict


def increase_level_numbers(_, __, event_dict):
    event_dict["level"] = event_dict["level_number"] * 10
    event_dict.pop("level_number", None)
    return event_dict


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

# if ddtrace_available:
#     processors.insert(0, tracer_injection)


def get_logger():
    structlog.configure(
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
        processors=processors,
    )
    bufflog = structlog.get_logger()
