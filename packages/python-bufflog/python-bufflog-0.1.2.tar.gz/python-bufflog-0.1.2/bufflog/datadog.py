try:
    import ddtrace
    from ddtrace.helpers import get_correlation_ids

    ddtrace_available = True
except ImportError:
    ddtrace_available = False


def is_ddtrace_available():
    return ddtrace_available


def tracer_injection(logger, log_method, event_dict):
    # get correlation ids from current tracer context
    trace_id, span_id = get_correlation_ids()

    # Add ids to Structlog event dictionary
    event_dict["dd.trace_id"] = trace_id or 0
    event_dict["dd.span_id"] = span_id or 0

    # add the env, service, and version configured for the tracer
    event_dict["dd.env"] = ddtrace.config.env or ""
    event_dict["dd.service"] = ddtrace.config.service or ""
    event_dict["dd.version"] = ddtrace.config.version or ""

    return event_dict