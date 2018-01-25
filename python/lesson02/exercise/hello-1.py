# Context and Tracing Functions
# -----------------------------
#
# Creating different spans for separate func

import sys
import time

from lib.tracing import init_tracer


# from lesson 01
def say_hello1(hello_to):
    """ one span for say_hello1
    """
    with tracer.start_span('say-hello') as span:
        span.set_tag('hello-to', hello_to)
        hello_str = format_string1(span, hello_to)
        print_hello1(span, hello_str)

def format_string1(span, hello_to):
    """ func doesn't have a separate span, but only log a single kv based event
    """
    hello_str = 'Hello, %s!' % hello_to
    span.log_kv({'event': 'string-format', 'value': hello_str})
    return hello_str

def print_hello1(span, hello_str):
    print("")
    print("Func Start")
    print(hello_str)
    print("Func End")
    print("")
    span.log_kv({'event': 'println'})


# wrap func into own span
def say_hello2(hello_to):
    with tracer.start_span('say-hello') as span:
        span.set_tag('hello-to', hello_to)
        hello_str = format_string2(span, hello_to)
        print_hello2(span, hello_str)

def format_string2(root_span, hello_to):
    with tracer.start_span('format') as span:
        hello_str = 'Hello, %s!' % hello_to
        span.log_kv({'event': 'string-format', 'value': hello_str})
        return hello_str

def print_hello2(root_span, hello_str):
    with tracer.start_span('println') as span:
        print("")
        print("Func Start")
        print(hello_str)
        print("Func End")
        print("")
        span.log_kv({'event': 'println'})


# simple check
assert len(sys.argv) == 2

# init the tracer
tracer = init_tracer('02-hello-world')

# main func
hello_to = sys.argv[1]
say_hello1(hello_to)

# yield to IOLoop to flush the spans
time.sleep(2)
tracer.close()
