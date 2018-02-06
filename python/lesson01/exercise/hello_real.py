#!/usr/bin/env python

# key part tag and log the span:
# https://github.com/shwsun/opentracing-tutorial/tree/master/python/lesson01#annotate-the-trace-with-tags-and-logs
# OpenTracing semantic conventions:
# https://github.com/opentracing/specification/blob/master/semantic_conventions.md

import logging
import sys
import time

#import opentracing
from jaeger_client import Config


def init_tracer(service):
    """Tracer implementation that is general enough."""
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()

tracer = init_tracer('my-tracer')


def say_hello(hello_to):
    """Major difference is that here we use span logging etc."""
    span = tracer.start_span('my-span')
    # The operation name represents a class of spans. The recommended solution
    # is to annotate spans with tags or logs.
    print("Span starts")
    hello_str = 'Hello, %s!' % hello_to
    span.log_kv({'event': 'string-format', 'value': hello_str})
    print(hello_str)
    span.log_kv({'event': 'println'})
    span.finish()
    print("Span ends")

# main
assert len(sys.argv) == 2

hello_to = sys.argv[1]
say_hello(hello_to)

# yield to IOLoop to flush the spans
time.sleep(1)
tracer.close()
