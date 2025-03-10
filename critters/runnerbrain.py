import numpy as np

from itertools import zip_longest

# This is the class where the actual "meat" of the genetic algorithm will take place!!
class RunnerBrain():
    
    # first generation constructor!!
    def __init__(self):
        # initial biases (starting with a preference for north and random)
        self.initial_bias = (0.2, 0.0, 0.0, 0.0, 0.1)
        # weightings for each kind of critter
        self.recognized_weightings = {
            # "Hunter": tuple(0.0 for i in range(10)), # a completely neutral opinion on hunters
            "Hunter": (0, 0, 0.2, 0.2, 0, 0, 0.2, 0.2, 0, 0), # a tendency to move to the side when a hunter is near
            "Runner": tuple(0.0 for i in range(10)),
        }
        # weightings for unrecognized agents (ie obstacles and corpses lol)
        self.unrecognized_weightings = tuple(0.0 for i in range(10))
            
    def think(self, move_weights: np.ndarray, vision = []):
        # add initial biases
        for i in range(len(move_weights)):
            move_weights[i] += self.initial_bias[i]
        
        # add decision weights
        decision_weights: set
        weight_to_add: float
        
        for item in vision:
            decision_weights = self.recognized_weightings.get(item[3], self.unrecognized_weightings)
            
            for i in range(len(move_weights)):
                weight_to_add = (item[0] * decision_weights[2*i]) + (item[1] * decision_weights[(2*i)+1])
                weight_to_add *= (1 + item[2]) 
                move_weights[i] += weight_to_add