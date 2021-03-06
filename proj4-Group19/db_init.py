"""
Generate random user data and populate db
"""
from mysql.connector import errorcode
import pandas as pd
from mysql import connector
from getpass import getpass
import os
import random
import hashlib
import string_utils

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
def generate_customers(amount=2000, refresh=True):
    """
    returns (str) customer data path
    """
    if not refresh:
        return f"{DIR_PATH}\\data\\customers.txt"
    customers = []
    with open(f"{DIR_PATH}\\data\\firstnames.txt", "r", encoding="utf8") as fname_file, open(f"{DIR_PATH}\\data\\lastnames.txt", "r", encoding="utf8") as lname_file:
        fnames = fname_file.readlines()
        lnames = lname_file.readlines()
    for i in range(amount):
        cid = amount + i # arbitrary
        fname = fnames[random.randint(0, len(fnames))].strip()
        lname = lnames[random.randint(0, len(lnames))].strip()
        phone = random.randint(1013108101, 91230099128) # arbitrary
        email = fname[0] + lname[0] + str(random.randint(0, 99)) + '@gmail.com'
        email = "".join(email.split(" "))
        password = hashlib.sha256((string_utils.shuffle(fname) + string_utils.shuffle(lname) + str(random.randint(0000, 9999))).encode()).digest()
        customers.append(f"{cid}\t{fname}\t{lname}\t{password}\t{phone}\t{email}\n")
    with open(f"{DIR_PATH}\\data\\customers.txt", "w", encoding="utf8") as customers_file:
        for customer in customers:
            customers_file.write(customer)
    return f"{DIR_PATH}\\data\\customers.txt"


def populate_customers(cursor, path):
    query = "INSERT INTO customers (cid, firstname, lastname, password, phone, email) VALUES (%s, %s, %s, %s, %s, %s)"
    with open(path, "r", encoding="utf8") as customers_file:
        customers = customers_file.readlines()
    for i in range(len(customers)):
        customers[i] = customers[i].split("\t")
    cursor.executemany(query, customers)
    cursor.fetchall()
    print(cursor.rowcount, "records inserted")

def populate_clothes(cursor):
        query = "INSERT INTO CLOTHES (clid, clname, color, size, category, price, qty_in_stock) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data = pd.read_csv(f'{DIR_PATH}\\data\\clothes.csv', index_col=False, delimiter = ',')
        data.head()
        for i,row in data.iterrows():
            cursor.execute(query, tuple(row))

def populate_admins(cursor):
        query = "INSERT INTO customers (firstname, lastname, password, phone, email, administrator) VALUES ('Raquel', 'Pereda', 'pass123', '813-123-4567', 'raquelpereda@gmail.com', TRUE)"
        cursor.execute(query)

def init(db_name, default=False):
    password = getpass("Enter root password: ")
    try:
        db = connector.connect(
            host="localhost",
            user="root",
            passwd=password,
            database=db_name
        )
    except connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid password")
            raise err
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Database {db_name} does not exist")
            yes = input("Would you like to create a new database? (y/n): ").lower().startswith("y")
            if yes:
                db = connector.connect(
                    host="localhost",
                    user="root",
                    passwd=password
                )
                db.cursor().execute(f"CREATE DATABASE {db_name}")
                cursor = db.cursor()
                cursor.execute(f"SHOW DATABASES")
                cursor.fetchall()
                db.close()
                db = connector.connect(
                    host="localhost",
                    user="root",
                    passwd=password,
                    database=db_name
                )
                default = True
            else:
                raise err
        else:
            raise err
    if default:
        cursor =db.cursor()
        with open(f'{DIR_PATH}\\setup.sql', 'r') as file:
            commands = file.read()
            cursor.execute(commands)
            cursor.close()
        
        cursor =db.cursor()
        with open(f'{DIR_PATH}\\setup1.sql', 'r') as file:
            commands1 = file.read()
            cursor.execute(commands1)
            cursor.close()

        cursor =db.cursor()
        with open(f'{DIR_PATH}\\setup2.sql', 'r') as file:
            commands2 = file.read()
            cursor.execute(commands2)
            cursor.close()
        db.commit()
        
    return db

def setup(cursor):
    with open(f'{DIR_PATH}\\setup.sql', 'r') as file:
        commands = file.read()
    try:
        cursor.execute(commands)
    except connector.Error as err:
        raise err

def default_init(db_name):
    db = init(db_name, True)
    populate_clothes(db.cursor())
    populate_customers(db.cursor(), generate_customers(refresh=False))
    populate_admins(db.cursor())
    db.commit()
    db.close()
    print("Successfully initialized database")
    

if __name__ == '__main__':
    default_init(input("Enter database name: "))