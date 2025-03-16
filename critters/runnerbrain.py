import numpy as np
import random as rand

from itertools import chain

GENOME_SIZE = 35

# This is the class where the actual "meat" of the genetic algorithm will take place!!
class RunnerBrain():
    
    # first generation constructor!!
    def __init__(self, parents=[], mutation_ratio=0.5, mutation_strength=0.2):
        # first generation
        genes = [0 for i in range(GENOME_SIZE)]
        parent_count = len(parents)
        
        if 1 == parent_count: # ASEXUAL
            genes = parents[0].gene_dump()
        elif 1 < parent_count: # SEXUAL
            #! SKELETAL
            parent_genes = chain(parent.gene_dump for parent in parents)
        else: # IMMACULATE CONCEPTION IDFK
            # Executive decision to add an initial bias against going backwards and towards going forward in the first generation
            # otherwise we'll never get anywhere
            genes[0] = 0.2
            genes[2] = -0.2
            genes[4] = 0.2
        
        self.apply_mutation(genes, mutation_ratio, mutation_strength)
        
        self.initial_bias = tuple(genes[0: 5])
        # weightings for each kind of critter
        self.hunter_weightings = tuple(genes[5: 15])
        self.runner_weightings = tuple(genes[15: 25])
        # weightings for obstacles and other unrecognized agents
        self.obstacle_weightings = tuple(genes[25: 35])
        
        # Map to make life easier
        self.recognition_map = {
            "Hunter": self.hunter_weightings,
            "Runner": self.runner_weightings
        }
            
    def think(self, move_weights: np.ndarray, vision = []):
        # add initial biases
        for i in range(len(move_weights)):
            move_weights[i] += self.initial_bias[i]
        
        # add decision weights
        decision_weights: set
        weight_to_add: float
        
        for item in vision:
            decision_weights = self.recognition_map.get(item[3], self.obstacle_weightings)
            
            for i in range(len(move_weights)):
                weight_to_add = (item[0] * decision_weights[2*i]) + (item[1] * decision_weights[(2*i)+1])
                weight_to_add *= (1 + item[2]) 
                move_weights[i] += weight_to_add
    
    def apply_mutation(self, genes, mutation_ratio, mutation_strength):
        for i in range(len(genes)):
            if rand.random() > mutation_ratio:
                continue
            
            genes[i] += (rand.random() * mutation_strength * 2) - mutation_strength
    
    def gene_dump(self) -> list[float]:
        genes = [g for g in 
            self.initial_bias + 
            self.hunter_weightings + 
            self.runner_weightings + 
            self.obstacle_weightings
        ]
        
        return genes
        