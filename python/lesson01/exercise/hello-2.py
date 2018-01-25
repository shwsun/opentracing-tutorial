import logging
import sys
import time

from jaeger_client import Config

import opentracing


def init_tracer(service):
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


def say_hello(hello_to):
    """ start and end a tracer for the func
    """
    span = tracer.start_span('01-say-hello')
    hello_str = 'Hello, %s!' % hello_to
    print("")
    print("Func Start")
    print(hello_str)
    print("Func End")
    print("")
    span.finish()


def say_hello2(hello_to):
    """ hello2 and hello are the same
    """
    with tracer.start_span('01-say-hello') as span:
        hello_str = 'Hello, %s!' % hello_to
        print("")
        print("Func Start")
        print(hello_str)
        print("Func End")
        print("")


# init the tracer
# ---------------
# the two tracers are the same
tracer = opentracing.tracer
tracer = init_tracer('hello-world')

# main
hello_to = sys.argv[1]
say_hello(hello_to)
