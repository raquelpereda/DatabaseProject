import sys
import hashlib
from getpass import getpass
from cart import Cart
from datetime import datetime
from db_init import init

class Customer:
    def __init__(self, data):
        self.cid = data[0]
        self.firstname = data[1]
        self.lastname = data[2]
        self.phone = data[3]
        self.email = data[4]
        self.cart = Cart()
    


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

def searchClothes2(db, data):
    cursor = db.cursor()
    query = "SELECT * FROM clothes WHERE "
    for i, item in enumerate(data["category"]):
        query += f"category='{item}' "
        if i != len(data["category"]) -1:
            query += "OR "
    end = False
    if len(data["size"]) > 0:
        query += " AND ("
        end = True
    for i, item in enumerate(data["size"]):
        query += f"size='{item}' "
        if i != len(data["size"]) -1:
            query += "OR "
    if end:
        query += ")"
        end = False
    if len(data["color"]) > 0:
        query += " AND ("
        end = True
    for i, item in enumerate(data["color"]):
        query += f"color='{item}' "
        if i != len(data["color"]) -1:
            query += "OR "              
    if end:
            query += ")"
            end = False
    if len(data["category"]) < 1 and len(data["size"]) < 1 and len(data["color"]) < 1:
        query = "SELECT * FROM clothes"
    # print(query)
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def buy(db, customer, cardNum):
    cursor = db.cursor()
    transaction_query = "INSERT INTO transaction (cid, clid, date, cardNum, qty) VALUES (%s, %s, %s, %s, %s)"
    check_availability = "SELECT qty_in_stock from clothes where clid = %s"
    decrement_qry = "UPDATE clothes SET qty_in_stock = qty_in_stock - %s where clid= %s"
    
    for item, qty in customer.cart.items:
        cursor.execute(check_availability, (item.clid,))
        qty_avail = cursor.fetchone()
        if qty_avail >= qty:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(decrement_qry, (qty, item.clid))
            cursor.execute(transaction_query, (customer.cid, item.clid, now, 12345, qty))
            customer.cart.remove_item(item, all=True)
        else:
            print("Item not in stock")

if __name__ == "__main__":
    b = {'category': ['T-Shirt', 'Dress'], 'size': ['Small', 'Large'], 'color': ['Green', 'Brown', 'Purple']}
    db = init("test_db")
    print(searchClothes2(db, b))
