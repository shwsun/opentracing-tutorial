#!/usr/bin/env python

# Key ideas:
# 1. capture causal relationship

import sys
import time

from opentracing_instrumentation.request_context import (get_current_span,
                                                         span_in_context)

from lib.tracing import init_tracer


def say_hello(hello_to):
    with tracer.start_span('my-span--say-hello') as span:
        span.set_tag('my-tag--hello-to', hello_to)
        hello_str = format_string(span, hello_to)
        print_hello(span, hello_str)

def format_string_prev(span, hello_to):
    """Causal relationship is not captured. Spans are not stiched into one full
    trace.
    """
    with tracer.start_span('my-span--format') as span:
        hello_str = 'Hello, %s!' % hello_to
        span.log_kv({'event': 'string-format', 'value': hello_str})
        return hello_str

def format_string(root_span, hello_to):
    """Function that """
    with tracer.start_span('format', child_of=root_span) as span:
        hello_str = 'Hello, %s!' % hello_to
        span.log_kv({'event': 'string-format', 'value': hello_str})
        return hello_str

def print_hello(root_span, hello_str):
    with tracer.start_span('my-span--println', child_of=root_span) as span:
        print(hello_str)
        span.log_kv({'event': 'println'})


assert len(sys.argv) == 2

tracer = init_tracer('my-tracer--hello-world')

hello_to = sys.argv[1]
say_hello(hello_to)

# yield to IOLoop to flush the spans
time.sleep(2)
tracer.close()

# I can't see two log msgs?
