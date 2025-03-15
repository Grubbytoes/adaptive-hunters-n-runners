import numpy as np

from itertools import zip_longest

# This is the class where the actual "meat" of the genetic algorithm will take place!!
class RunnerBrain():
    
    # first generation constructor!!
    def __init__(self, parents=[], mutation_ratio=0.2):
        # initial biases (starting with a preference for north and random)
        self.initial_bias = (0.2, 0.0, 0.0, 0.0, 0.1)
        # weightings for each kind of critter
        self.hunter_weightings = tuple(0.0 for i in range(10))
        self.runner_weightings = tuple(0.0 for i in range(10))
        # weightings for obstacles and other unrecognized agents
        self.obstacle_weightings = tuple(0.0 for i in range(10))
        
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
    
    def gene_dump(self) -> list[float]:
        genes = [g for g in 
            self.initial_bias + 
            self.hunter_weightings + 
            self.runner_weightings + 
            self.obstacle_weightings
        ]
        
        return genes
        