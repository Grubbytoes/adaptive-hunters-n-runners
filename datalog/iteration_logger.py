from .abstract_logger import AbstractLogger

# TODO
class IterationLogger(AbstractLogger):

    def __init__(self):
        super().__init__()
        self.generations = []
        self.params = None
        self.payload = {
            "params": self.params,
            "generations": self.generations
        }

    def enter_params(self, params):
        self.params = params

    def read(self, other):
        self.generations.append(other.copy_payload())

    def clear(self):
        self.generations.clear()