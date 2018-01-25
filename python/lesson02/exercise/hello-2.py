import sys
import time
from lib.tracing import init_tracer


def say_hello(hello_to):
    with tracer.start_span('say-hello') as span:
        span.set_tag('hello-to', hello_to)
        hello_str = format_string(span, hello_to)
        print_hello(span, hello_str)


def format_string(root_span, hello_to):
    with tracer.start_span('format') as span:
        hello_str = 'Hello, %s!' % hello_to
        span.log_kv({'event': 'string-format', 'value': hello_str})
        return hello_str


def print_hello(root_span, hello_str):
    with tracer.start_span('println') as span:
        print(hello_str)
        span.log_kv({'event': 'println'})


# main
assert len(sys.argv) == 2

tracer = init_tracer('hello-world')

hello_to = sys.argv[1]
say_hello(hello_to)

# yield to IOLoop to flush the spans
time.sleep(2)
tracer.close()
