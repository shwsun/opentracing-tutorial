# lesson01/exercise/hello.py
import sys

def say_hello(hello_to):
    hello_str = 'Hello, %s!' % hello_to
    print(hello_str)


# main
assert len(sys.argv) == 2
print(sys.argv)
hello_to = sys.argv[1]
say_hello(hello_to)
