import sys
import hashlib
from getpass import getpass
from cart import Cart
from datetime import datetime
from db_init import init

class Admin:
    def __init__(self, data):
        