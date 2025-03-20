import json

class AbstractLogger:
    
    def __init__(self):
        self.payload: dict
    
    def read(self, other):
        raise NotImplementedError("read method not implemented!!")
           
    def dump(self, indent=None):
        return json.dumps(self.payload, indent=indent)
    
    def copy_payload(self):
        return self.payload.copy()