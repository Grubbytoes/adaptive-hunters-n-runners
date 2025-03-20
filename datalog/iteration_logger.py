from .abstract_logger import AbstractLogger

# TODO
class IterationLogger(AbstractLogger):

    def __init__(self):
        super().__init__()
        self.generations = []
        self._param_data = None
        
        self.payload = {
            "generations": self.generations
        }

    def set_param_data(self, params):
        self._param_data = params
    
    def get_param_data(self):
        return tuple(self._param_data)

    def read(self, other):
        self.generations.append(other.copy_payload())

    def clear(self):
        self.generations.clear()