import sys
import hashlib
from getpass import getpass
from cart import Cart
from datetime import datetime
from db_init import init

class Admin:
    def __init__(self, data):
        self.cid = data[0]
        self.firstname = data[1]
        self.lastname = data[2]
        self.phone = data[3]
        self.email = data[4]