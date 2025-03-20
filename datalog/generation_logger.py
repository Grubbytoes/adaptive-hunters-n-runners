import json

from .runner_logger import RunnerLogger, empty_gene_dict

# TODO unifinished
class GenerationLogger():
    def __init__(self):
        self.population: list[RunnerLogger]
        self.genetic_average: tuple
    
    def read_population(self, *runners: RunnerLogger):
        self.population.clear()
        self.population = list(runners)
        self.genetic_average = empty_gene_dict()
        
        raw_genetic_data = []
    