from item import Item

class Cart:
    def __init__(self):
        self.items = dict() # item : qty
    
    def add_item(self, item):    
        if item in self.items:
            self.items[item] += 1
        else:
            self.items[item] = 1
    
    def remove_item(self, item, all=False):
        if item in self.items:
            if all:
                del self.items[item]
            else:
                if self.items[item] > 1:
                    self.items[item] -= 1
                else:
                    del self.items[item]

    def total(self):
        total = 0
        for item, qty in self.items:
            total += item.price * qty
        return total
