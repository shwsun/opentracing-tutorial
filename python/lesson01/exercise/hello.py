#!/usr/bin/env python

# lesson01/exercise/hello.py
import sys

import opentracing


def say_hello(hello_to):
    """Plain hello world"""
    hello_str = 'Hello, %s!' % hello_to
    print(hello_str)


tracer = opentracing.tracer

def say_hello_traced(hello_to):
    """Hello world but with tracing"""
    span = tracer.start_span('say-hello')
    print("Span started")
    hello_str = 'Hello, %s!' % hello_to
    print(hello_str)
    span.finish()
    print("Span ends")


def say_hello_retraced(hello_to):
    with tracer.start_span('say-hello') as span:
        print("Span starts here")
        hello_str = 'Hello, %s!' % hello_to
        print(hello_to)
        print("Span ends automatically")


assert len(sys.argv) == 2

hello_to = sys.argv[1]

print("\n\nHello-world #1:\n")
say_hello(hello_to)
print("\n\nHello-world #2:\n")
say_hello_traced(hello_to)
print("\n\nHello-world #3:\n")
say_hello_retraced(hello_to)
