#!/usr/bin/env python3
'''
General utilities
'''
import os
import base64
import binascii

def get_random_number(length=32):
    '''
    Get a random value.
    :param length: length of the random number, in bytes
    :return: hexlified string.
    '''
    return binascii.hexlify(os.urandom(length)).decode()

if __name__ == "__main__":
    rand = get_random_number()
    print("Got rand: {}".format(rand))
