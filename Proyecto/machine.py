class Pin:
    OUT = None
    value_ = 0
    
    def __init__(self, pin, mode = None):
        self.pin = pin
        self.mode = mode
    
    def value(self, n = None):
        if n == 0 or n == 1:
            self.value_ = n
        else:
            return self.value_            
                
    def __str__(self):
        return f"Pin({self.pin}, mode={self.mode})"