"""
Application representation of customer
"""
import sys
import hashlib
from getpass import getpass
#TODO: add email
class Customer:
    def __init__(self, email, password_hash, db):
        self.email = email
        self.password_hash = hashlib.sha256(password_hash.encode()).digest()
        self.db_handle = db
        data = login(db, (self.email, self.password_hash))
        try:
            self.cid, self.firstname, self.lastname, _, self.phone = data[0]
        except:
            print("Invalid email or password")
            sys.exit(1)

def sign_up(db, data=None): # to receive data from webpage
    if not data:
        data = dict()
        data["firstname"] = input("Enter firstname: ")
        data["lastname"] = input("Enter lastname: ")
        # data["email"] = input("Enter email: ")
        data["password"] = hashlib.sha256(getpass("Enter password: ").encode()).digest()
        #TODO: Re-enter password
        data["phone"] = int(input("Enter phone: ")) #TODO: parse numbers robustly
    query = "INSERT INTO customers (firstname, lastname, password, phone) VALUES (%s, %s, %s, %s)"
    cursor = db.cursor()
    cursor.execute(query, tuple(data.values()))
    db.commit()

def login(db, data=None):
    cursor = db.cursor()
    query = "SELECT * FROM customers WHERE firstname=%s and password=%s"
    if data:
        cursor = db.cursor()
        cursor.execute(query, data)
        results = cursor.fetchall()
        return results

    firstname = input("Enter first name: ") #TODO: use email
    password_hash = hashlib.sha256(getpass("Enter password: ").encode()).digest() # TODO: make util
    cursor.execute(query, (firstname, password_hash))
    results = cursor.fetchall()
    return results