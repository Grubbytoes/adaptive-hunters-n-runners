import numpy as np
import random as rand

from itertools import chain

GENOME_SIZE = 29

print("wtf")

global_mutation_ratio = 0.0
global_mutation_strength = 0.0

# This is the class where the actual "meat" of the genetic algorithm will take place!!
class RunnerBrain():
    
    # first generation constructor!!
    def __init__(self, parents=[]):
        # first generation
        genes = [0 for i in range(GENOME_SIZE)]
        parent_count = len(parents)
        
        if 1 == parent_count: # ASEXUAL
            genes = parents[0].gene_dump()
        elif 1 < parent_count: # SEXUAL
            #! UNTESTED
            parent_gene_chain = []
            for p in parents:
                parent_gene_chain += p.gene_dump()
            parent_gene_chain = tuple(parent_gene_chain)
            
            for i in range(GENOME_SIZE):
                inherited_gene = parent_gene_chain[i + rand.randint(0, parent_count-1) * GENOME_SIZE]
                genes[i] = inherited_gene
        else: # IMMACULATE CONCEPTION IDFK
            # Executive decision to add an initial bias against going backwards and towards going forward in the first generation
            # otherwise we'll never get anywhere
            genes[0] = 0.1
            genes[2] = -0.1
        
        self.apply_mutation(genes)
        
        self.initial_bias = tuple(genes[0: 4])
        # weightings for each kind of critter
        self.hunter_weightings = tuple(genes[4: 12])
        self.runner_weightings = tuple(genes[12: 20])
        # weightings for obstacles and other unrecognized agents
        self.obstacle_weightings = tuple(genes[20: 28])
        # impulsiveness
        self.impulsiveness = genes[28]
        
        # Map to make life easier
        self.recognition_map = {
            "Hunter": self.hunter_weightings,
            "Runner": self.runner_weightings
        }
            
    def think(self, move_weights: np.ndarray, vision = []): 
        # roll for impulse(ivness)
        if (rand.random() * 2 - 1) < self.impulsiveness:
            move_weights[4] = 10
            return
        else:
            move_weights[4] = -10
               
        # add initial biases
        for i in range(4):
            move_weights[i] += self.initial_bias[i]
        
        # add decision weights
        decision_weights: set
        weight_to_add: float
        
        for item in vision:
            decision_weights = self.recognition_map.get(item[3], self.obstacle_weightings)
            
            for i in range(4):
                weight_to_add = (item[0] * decision_weights[2*i]) + (item[1] * decision_weights[(2*i)+1])
                weight_to_add *= (1 + item[2]) 
                move_weights[i] += weight_to_add
    
    def apply_mutation(self, genes):
        for i in range(len(genes)):
            if rand.random() > global_mutation_ratio:
                continue
            
            genes[i] += (rand.random() * global_mutation_strength * 2) - global_mutation_strength
            
            # clamp between -1 and 1
            genes[i] = min(max(-1.0, genes[i]), 1.0)
    
    def gene_dump(self) -> list[float]:
        genes = [g for g in 
            self.initial_bias + 
            self.hunter_weightings + 
            self.runner_weightings + 
            self.obstacle_weightings
        ]
        
        genes.append(self.impulsiveness)
        
        return genes


def set_mutation_params(ratio, strength):
    global global_mutation_ratio, global_mutation_strength
    
    global_mutation_ratio = ratio
    global_mutation_strength = strength