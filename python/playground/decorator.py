#!/usr/bin/env python3

def decorate_den_less_than_num(function):
    print "Decorator to check denominator less than numerator applied"
    def check_den_less_than_num(num, den):
        if den>num:
            print "Denominator > Numerator. So dont call the actual function"
            return 0
        else:
            print "Denominator <= Numerator. So call actual function"
            return function(num, den)
    return check_den_less_than_num


@decorate_den_less_than_num
def divide(numerator, denominator):
    print(numerator/denominator)


# main
divide(4, 2)
divide(4, 5)

