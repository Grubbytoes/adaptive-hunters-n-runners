import numpy as np

from .abstract_logger import AbstractLogger
from .runner_logger import RunnerLogger, empty_gene_dict, readable_gene_dict

# TODO unifinished
class PopulationLogger(AbstractLogger):
    def __init__(self):
        super().__init__()
        
        self.population = []
        self.genetic_mean: tuple
        self.genetic_range: tuple

    def read(self, runners):
        raw_population = [RunnerLogger(r) for r in runners]
        raw_genetic_array = np.array([r.genes for r in raw_population])
        rotated_genetic_array = [raw_genetic_array[0:, i] for i in range(raw_genetic_array.shape[1])]
        
        self.genetic_mean = [np.mean(g) for g in rotated_genetic_array]
        self.genetic_range = [np.ptp(g) for g in rotated_genetic_array]
        self.population = [r.payload for r in raw_population]
        self.payload = {
            "population": self.population,
            "genetic mean": readable_gene_dict(self.genetic_mean),
            "genetic range": readable_gene_dict(self.genetic_mean)
        }
