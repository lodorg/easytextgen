
class Priority:
    
    def __init__(self, objects: list):
        self.items = objects
        
    def move_first(self, obj):
        if obj not in self.items:
            print(f"Warning: Object {obj} not in objects!")
        self.items.remove(obj)
        self.items.insert(0, obj)
        
    def get_first(self):
        return self.items[0]