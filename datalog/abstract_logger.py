import json

class AbstractLogger:
    
    def __init__(self):
        self.payload: dict
    
    def read(self):
        raise NotImplementedError("read method not implemented!!")
           
    def dump(self):
        return json.dumps(self.payload, indent=2)