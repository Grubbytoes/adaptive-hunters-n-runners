from .abstract_logger import AbstractLogger
from .runner_logger import RunnerLogger, empty_gene_dict, readable_runner_dict

# TODO unifinished
class PopulationLogger(AbstractLogger):
    def __init__(self):
        super().__init__()
        
        self.population = []
        self.genetic_average: tuple
        self.genetic_range: tuple

    def read(self, runners):
        raw_population = [RunnerLogger(r) for r in runners]

        self.population = [r.payload for r in raw_population]
        self.genetic_average = empty_gene_dict()
        
        self.payload = {
            "population": self.population
        }

    def write_population_log(self):
        return json.dumps(self.payload)
