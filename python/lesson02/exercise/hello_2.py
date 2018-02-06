#!/usr/bin/env python

# Key ideas:
# 1. capture causal relationship
# 2. context propagation for python
# https://github.com/yurishkuro/opentracing-tutorial/tree/master/python/lesson02#propagate-the-in-process-context

import sys
import time

from opentracing_instrumentation.request_context import (get_current_span,
                                                         span_in_context)

from lib.tracing import init_tracer


def say_hello_prev(hello_to):
    with tracer.start_span('my-span--say-hello') as span:
        span.set_tag('my-tag--hello-to', hello_to)
        hello_str = format_string(span, hello_to)
        print_hello(span, hello_str)

def say_hello(hello_to):
    with tracer.start_span('say-hello') as span:
        span.set_tag('hello-to', hello_to)
        with span_in_context(span):
            hello_str = format_string(hello_to)
            print_hello(hello_str)

def format_string_prev_again(span, hello_to):
    """Causal relationship is not captured. Spans are not stiched into one full
    trace.
    """
    with tracer.start_span('my-span--format') as span:
        hello_str = 'Hello, %s!' % hello_to
        span.log_kv({'event': 'string-format', 'value': hello_str})
        return hello_str

def format_string_prev(root_span, hello_to):
    """Function that """
    with tracer.start_span('format', child_of=root_span) as span:
        hello_str = 'Hello, %s!' % hello_to
        span.log_kv({'event': 'string-format', 'value': hello_str})
        return hello_str

def format_string(hello_to):
    """Function that """
    root_span = get_current_span()
    with tracer.start_span('format', child_of=root_span) as span:
        hello_str = 'Hello, %s!' % hello_to
        span.log_kv({'event': 'string-format', 'value': hello_str})
        return hello_str

def print_hello_prev(root_span, hello_str):
    with tracer.start_span('my-span--println', child_of=root_span) as span:
        print(hello_str)
        span.log_kv({'event': 'println'})

def print_hello(hello_str):
    root_span = get_current_span()
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
