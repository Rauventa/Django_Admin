import binascii
import os


def get_random_token():
    return binascii.hexlify(os.urandom(20)).decode()
