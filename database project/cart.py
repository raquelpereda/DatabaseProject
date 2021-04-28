import item.Item

class Cart:
    def __init__(self):
        self.items = dict() # item : qty
    
    def add_item(self, item):
        if item.qty_in_stock < 1:
            # raise error
            return False
            
        if item in self.items:
            self.items[item] += 1
        else:
            self.items[item] = 1
    
    def remove_item(self, item):
        if item in self.items:
            del self.items[item]
        else:
            # throw error
            pass
    
    def total(self):
        total = 0
        for item, qty in self.items:
            total += item.price * qty
        return total