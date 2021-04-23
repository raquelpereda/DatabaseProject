import sys
import hashlib
from getpass import getpass

class Customer:
    def __init__(self, email, password_hash, db):
        self.email = email
        self.password_hash = hashlib.sha256(password_hash.encode()).digest()
        self.db_handle = db
        data = log_in(db, (self.email, self.password_hash))
        try:
            self.cid, self.firstname, self.lastname, _, self.phone = data[0]
        except:
            print("Invalid email or password")
            sys.exit(1)

def sign_up(db, data=None):
    # TODO: check if user already exists
    cursor = db.cursor()
    query = "INSERT INTO customers (firstname, lastname, email, password, phone) VALUES (%s, %s, %s, %s, %s)"
    if not data:
        data = dict()
        data["firstname"] = input("Enter firstname: ")
        data["lastname"] = input("Enter lastname: ")
        data["email"] = input("Enter email: ")
        data["password"] = hashlib.sha256(getpass("Enter password: ").encode()).digest()
        #TODO: Re-enter password
        data["phone"] = int(input("Enter phone: ")) #TODO: parse numbers robustly
    cursor = db.cursor()
    data['password'] = hashlib.sha256(data['password'].encode()).digest()
    cursor.execute(query, (data['firstname'], data['lastname'], data['email'], data['password'], data['phone']))
    db.commit()

def log_in(db, data=None):
    cursor = db.cursor()
    query = "SELECT * FROM customers WHERE email=%s and password=%s"
    if not data:
        data = dict()
        data["email"] = input("Enter email: ")
        data["password"] = hashlib.sha256(getpass("Enter password: ").encode()).digest()
    cursor = db.cursor()
    data['password'] = hashlib.sha256(data['password'].encode()).digest()
    cursor.execute(query, (data['email'], data['password']))
    results = cursor.fetchone()
    return results