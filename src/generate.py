"""
Generate random user data and populate db
"""
from mysql.connector import errorcode
from mysql import connector
from getpass import getpass
import os
import random
import hashlib
import string_utils
import customer

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

def generate_customers(amount=2000):
    customers = []
    with open(f"{DIR_PATH}\\data\\firstnames.txt", "r", encoding="utf8") as fname_file, open(f"{DIR_PATH}\\data\\lastnames.txt", "r", encoding="utf8") as lname_file:
        fnames = fname_file.readlines()
        lnames = lname_file.readlines()
    for i in range(amount):
        cid = amount + i # arbitrary
        fname = fnames[random.randint(0, len(fnames))].strip()
        lname = lnames[random.randint(0., len(lnames))].strip()
        phone = random.randint(1013108101, 91230099128) # arbitrary
        #TODO: add email
        # email = fname[0] + lname[0] + str(random.randint(0, 99)) + '@gmail.com'
        password = hashlib.sha256((string_utils.shuffle(fname) + string_utils.shuffle(lname) + str(random.randint(0000, 9999))).encode()).digest()
        customers.append(f"{cid}\t{fname}\t{lname}\t{password}\t{phone}\n")
    with open(f"{DIR_PATH}\\data\\customers.txt", "w") as customers_file:
        for customer in customers:
            customers_file.write(customer)

def populate_customers(cursor):
    query = "INSERT INTO customers (cid, firstname, lastname, password, phone) VALUES (%s, %s, %s, %s, %s)"
    with open(f"{DIR_PATH}\\data\\customers.txt", "r") as customers_file:
        customers = customers_file.readlines()
    for i in range(len(customers)):
        customers[i] = customers[i].split("\t")
    cursor.executemany(query, customers)
    print(cursor.rowcount, "records inserted")

def init(default=False):
    password = getpass("Enter password: ")
    try:
        db = connector.connect(
            host="localhost",
            user="root",
            passwd=password,
            database="datacamp"
        )
    except connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid password\n")
            raise err
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist\n")
        else:
            print(err)

    if default:
        setup(db.cursor())
    return db

def setup(cursor):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{dir_path}\\setup.sql', 'r') as file:
        commands = file.read()
    try:
        cursor.execute(commands)
    except connector.Error as err:
        # TODO: handle
        raise err

def main():
    db = init()
    # c = customer.Customer(name, passwd, db)
    db.close()

if __name__ == '__main__':
    main()