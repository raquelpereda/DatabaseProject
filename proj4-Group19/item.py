class Item:
    def __init__(self, data):
        self.clid = data[0]
        self.clname = data[1]
        self.color = data[2]
        self.size = data[3]
        self.category = data[4]
        self.price = data[5]
        self.qty = data[6]

def get_item(db, clid):
    cursor = db.cursor()
    query = "SELECT * from clothes where clid=%s"
    cursor.execute(query, (clid,))
    return cursor.fetchone()
    