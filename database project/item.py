class Item:
    def __init__(self, data):
        self.clid = data["clid"]
        self.clname = data["clname"]
        self.color = data["color"]
        self.size = data["size"]
        self.category = data["category"]
        self.price = data["price"]
        self.qty = data["qty_in_stock"]
    