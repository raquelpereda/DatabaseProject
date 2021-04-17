"""
Application representation of customer
"""
import hashlib
#TODO: add email
class customer:
    def __init__(self, email, password, db):
        self.email = email
        self.password = password
        self.db_handle = db
    
    def login(self):
        password_hash = hashlib.sha256(password.encode()).digest()
        query = f"SELECT * FROM customers WHERE password={password_hash}"
        cursor = self.db_handle.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
