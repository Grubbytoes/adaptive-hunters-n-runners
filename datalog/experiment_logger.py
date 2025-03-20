from .abstract_logger import AbstractLogger
from .iteration_logger import IterationLogger

#! untested!!
class ExperimentLogger(AbstractLogger):
    
    def __init__(self):
        self.payload = dict()
    
    def read(self, other):
        if not isinstance(other, IterationLogger):
            raise TypeError("ExperimentLogger can only read IterationLogger objects!!")
        
        self.payload.update({
            other.get_param_data(): other.copy_payload()
        })
        
    def clear(self):
        self.payload.clear