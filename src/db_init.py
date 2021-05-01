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

def generate_clothes(amount=500, refresh=True):
    if not refresh:
        return f"{DIR_PATH}\\data\\clothes.txt"
        
    categories = {1:"accessory", 2:"bottom", 3:"top", 4:"shoes", 5:"one piece", 
                  6:"two piece", 7:"three piece", 8:"dress", 9:"over", 10:"underwear"}
    # cat = (baby, child, teen, adult, male, female, unisex)
    colors = ["red", "blue", "green", "yellow", "orange", "black", "white", "gray", "gold", "rose gold"]
    sizes = ["XXS", "XS", "S", "M", "L", "XL", "XXL"]
    clothes = []
    with open(f"{DIR_PATH}\\data\\brands.txt", "r", encoding="utf8") as brands_file:
        brands = brands_file.readlines()

    for i in range(amount):
        clid = amount + i
        clname = random.choice(brands).strip()
        color = random.choice(colors)
        size = random.choice(sizes)
        category = random.choice(list(categories.values()))
        price = round(random.uniform(4.99, 79.99), 2) #TODO: use weights
        qty = random.randint(1, 200)
        clothes.append(f"{clid}\t{clname}\t{color}\t{size}\t{category}\t{price}\t{qty}\n")
    with open(f"{DIR_PATH}\\data\\clothes.txt", "w", encoding="utf8") as clothes_file:
        for item in clothes:
            clothes_file.write(item)
    return f"{DIR_PATH}\\data\\clothes.txt"

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
        fname = fnames[random.randint(0, len(fnames)-1)].strip()[:44] # 44 for length limits
        lname = lnames[random.randint(0, len(lnames)-1)].strip()[:44]
        phone = random.randint(1013108101, 91230099128) # arbitrary
        #TODO: add email
        email = fname[0] + lname + str(random.randint(0, 99)) + '@gmail.com'
        email = "".join(email.split(" "))[:44]
        password = hashlib.sha256((string_utils.shuffle(fname) + string_utils.shuffle(lname) + str(random.randint(0000, 9999))).encode()).digest()
        customers.append(f"{cid}\t{fname}\t{lname}\t{password}\t{phone}\t{email}\n")
    with open(f"{DIR_PATH}\\data\\customers.txt", "w", encoding="utf8") as customers_file:
        for customer in customers:
            customers_file.write(customer)
    return f"{DIR_PATH}\\data\\customers.txt"

def populate_clothes(db, path):
    cursor = db.cursor()
    query = "INSERT INTO clothes (clid, clname, color, size, category, price, qty_in_stock) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    with open(path, "r", encoding="utf8") as clothes_file:
        clothes = clothes_file.readlines()
    for i in range(len(clothes)):
        clothes[i] = clothes[i].split("\t")
    cursor.executemany(query, clothes)
    cursor.fetchall()
    db.commit()
    print(cursor.rowcount, "clothes inserted")

def populate_customers(db, path):
    cursor = db.cursor()
    query = "INSERT INTO customers (cid, firstname, lastname, password, phone, email) VALUES (%s, %s, %s, %s, %s, %s)"
    with open(path, "r", encoding="utf8") as customers_file:
        customers = customers_file.readlines()
    for i in range(len(customers)):
        customers[i] = customers[i].split("\t")
    cursor.executemany(query, customers)
    cursor.fetchall()
    db.commit()
    print(cursor.rowcount, "customers inserted") #TODO: change to log

def init(db_name, default=False):
    password = getpass("Enter root password: ")
    try:
        db = connector.connect(
            host="localhost",
            user="root",
            passwd=password,
            database=db_name
        )
        if default:
            # TODO: drop if exists
            print(f"database already exists, returning connector for {db_name}")
            return db
        
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
        setup(db)
        db = connector.connect(
            host="localhost",
            user="root",
            passwd=password,
            database=db_name
        )
    return db

def setup(db):
    cursor = db.cursor()
    with open(f'{DIR_PATH}\\setup.sql', 'r') as file:
        commands = file.read()
    try:
        result = cursor.execute(commands, multi=True)
        for _ in result:
            pass
    except connector.Error as err:
        # TODO: handle
        raise err

def default_init(db_name):
    db = init(db_name, True)
    populate_customers(db, generate_customers())
    populate_clothes(db, generate_clothes())
    db.close()
    print("Successfully initialized database")

if __name__ == '__main__':
    default_init(input("Enter database name: "))