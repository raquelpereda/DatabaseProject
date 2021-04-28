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
    cursor = db.cursor()
    query = "SELECT * FROM customers WHERE email=%s"
    cursor = db.cursor()
    cursor.execute(query, (data['email'],))
    results = cursor.fetchone()
    
    if results:
        return ''
    
    cursor.close()
    query = "INSERT INTO customers (firstname, lastname, email, password, phone) VALUES (%s, %s, %s, %s, %s)"
    cursor = db.cursor(buffered = True)
    data['password'] = hashlib.sha256(data['password'].encode()).digest()
    cursor.execute(query, (data['firstname'], data['lastname'], data['email'], data['password'], data['phone']))
    db.commit()


def log_in(db, data=None):
    cursor = db.cursor()
    query = "SELECT * FROM customers WHERE email=%s and password=%s"
    cursor = db.cursor()
    data['password'] = hashlib.sha256(data['password'].encode()).digest()
    cursor.execute(query, (data['email'], data['password']))
    results = cursor.fetchone()
    return results

def searchClothes(db,data):
    cursor = db.cursor()
    print(data)
    if not data:
        cursor.execute("SELECT clname, price FROM clothes")
        allResults = cursor.fetchall()
        cursor.close()
        return allResults
    cursor = db.cursor(buffered = True)
    query = "SELECT clname, price FROM clothes WHERE size=%s AND category =%s AND color=%s"
    cursor.execute(query, (data[0], data[1], data[2]))
    results = cursor.fetchall()
    print(results)
    return results
