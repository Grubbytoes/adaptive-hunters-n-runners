import mesa
import numpy as np
import math


AVAILABLE_MOVES = ('N', 'E', 'S', 'W', 'R')

'''
    Superclass for hunters and runners.
'''
class Critter(mesa.Agent):

    def __init__(self, unique_id, model, x, y, sight_range = 1):
        super().__init__(unique_id, model)
        self.move_ind = 0
        self.next_move_weights = np.ones(5)
        self.type = "Undefined"
        self.initial_x = x
        self.initial_y = y

        # Vision
        self.sight_range = max(sight_range, 1)
        self.vision = []

    '''
        A function to print information about agents and their programs.
    '''
    def print_me(self):
        print("\nAgent, type:", self.type)
        print("Initial coords: (" + str(self.initial_x) + "," + str(self.initial_y) + ")")
        print("I can see: ", self.vision)

    def step(self):
        self.see()
        self.decide_move()
        self.do_move()
    
    def decide_move(self) -> None:
        self.next_move_weights = np.ones(5)
        introduce_noise(self.next_move_weights)

    '''
        Move agent, according to its program. Agents cannot occupy the same space as an obstacle, or other agent. 
    '''
    def do_move(self):
        introduce_noise(self.next_move_weights)
        move = AVAILABLE_MOVES[np.argmax(self.next_move_weights)]
        
        # initialise coordinates for next step to current location
        new_x = self.pos[0]
        new_y = self.pos[1]

        # set coordinates for attempted move - move may be blocked later, by obstacle or other agent
        if move == "R": # pick random location in Moore neighbourhood
            new_x = self.pos[0] + np.random.choice([-1, 0, 1])
            new_y = self.pos[1] + np.random.choice([-1, 0, 1])
        elif move == "N": # set y to row above 
            new_y = self.pos[1] + 1
        elif move == "S": # set y to row below
            new_y = self.pos[1] - 1
        elif move == "E": # set x to right column
            new_x = self.pos[0] + 1
        elif move == "W": # set x to left column
            new_x = self.pos[0] - 1
        else:
            print("Not a valid move!")

        if new_y < 0: # prevent agents from moving off bottom of grid
            new_y = 0
        elif new_y >= self.model.grid.height: # prevent agents from moving off top of grid
            new_y = self.model.grid.height - 1

        if new_x < 0: # prevent agents from moving off left of grid
            new_x = 0
        elif new_x >= self.model.grid.width: # prevent agents from moving off right of grid
            new_x = self.model.grid.width - 1

        # get obstacles and agents in Moore neighbourhood
        neighbours = self.model.grid.get_neighbors(self.pos, True)
        move = True
        for n in neighbours:
            if n.pos == (new_x, new_y): # prevent moving into cell with obstacle or other agent
                move = False    

        if move:        
            self.model.grid.move_agent(self, (new_x, new_y)) # move
            
        self.move_ind += 1 # increment program index
    
    def see(self): 
        # clear vision
        self.vision.clear()
        _thing = self.model.grid
        field_of_vision = _thing.get_neighbors(self.pos, True, radius=self.sight_range)
        
        for other in field_of_vision:
            x_relative = int(other.pos[0] - self.pos[0])
            y_relative = int(other.pos[1] - self.pos[1])
            magnitude = math.sqrt(math.pow(x_relative, 2) + math.pow(y_relative, 2))
            closeness = (self.sight_range - magnitude) / magnitude

            # vision entries are structured like so:
            #   [0] x component
            #   [1] y component
            #   [2] closeness, 0 being edge of vision, 1 being basically on top of you
            #   [3] agent type
            
            item = (
                x_relative / magnitude,
                y_relative / magnitude,
                closeness,
                other.type,
            )
            self.vision.append(item)


def introduce_noise(weights: np.ndarray, noise_amount=0.1):
    # Introduce noise to the weights
    for i in range(len(weights)):
        noise = 1 - noise_amount + (np.random.rand() * noise_amount * 2)
        weights[i] *= noise