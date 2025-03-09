import numpy as np

from itertools import zip_longest


class RunnerBrain():
    def __init__(self): # first generation constructor!!
        # initial biases (starting with a preference for north and random)
        self.alpha = (0.2, 0.0, 0.0, 0.0, 0.1)
        # weightings for each kind of critter
        self.bravo = {
            "Hunter": tuple(0.0 for i in range(10)),
            "Runner": tuple(0.0 for i in range(10)),
        }
        # weightings for unrecognized agents (ie obstacles and corpses lol)
        self.charlie = tuple(0.0 for i in range(10))
    
    def foo(self, move_weights: np.ndarray, vision = []):
        # add initial biases
        for i in range(len(move_weights)):
            move_weights[i] += self.alpha[i]
        
        # add decision weights
        decision_weights: set
        weight_to_add: float
        
        for item in vision:
            decision_weights = self.bravo.get(item[3], self.charlie)
            
            for i in range(len(move_weights)):
                weight_to_add = (item[0] * decision_weights[2*i]) + (item[1] * decision_weights[(2*i)+1])
                weight_to_add *= (1 + item[2]) 
                move_weights[i] += weight_to_add