class ConvertList(list):
    @classmethod
    def convert(cls, item):
        return item
    
    def __init__(self, items, convert=True):
        if convert:
            super().__init__([self.convert(item) for item in items])
        else:
            super().__init__(items)
            
    def __add__(self, items):
        return self.__class__(
            super().__add__([self.convert(item) for item in items]), 
            convert=False
        )
    
    def __getitem__(self, key):
        item = super().__getitem__(key)
        if isinstance(key, slice):
            return self.__class__(item, convert=False)
        return item
        
    def __iadd__(self, items):
        return super().__iadd__([self.convert(item) for item in items])
    
    def __imul__(self, val):
        return self.__class__(super().__imul__(val), convert=False)
    
    def __mul__(self, val):
        return self.__class__(super().__mul__(val), convert=False)
    
    def __setitem__(self, key, items):
        if isinstance(key, slice):
            items = [self.convert(item) for item in items]
        else:
            items = self.convert(items)
        super().__setitem__(key, items)
    
    def append(self, val):
        return super().append(self.convert(val))
    
    def copy(self):
        return self.__class__(super().copy(), convert=False)
    
    def extend(self, items):
        return super().extend([self.convert(item) for item in items])
    
    def insert(self, idx, val):
        return super().insert(idx, self.convert(val))