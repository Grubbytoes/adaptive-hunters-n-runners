from .critter import Critter
from random import randint

class Hunter(Critter):
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model, x, max(30, y), sight_range=8) # make all hunters start near the top of the environment
        self.type = "Hunter"
        self.timeout = 0
        self.energy = 8

    def decide_move(self):
        super().decide_move()

        # Lets have a look at those runners then!!
        for other in self.vision:
            if other[3] != "Runner":
                continue

            self.next_move_weights[0] += max(other[1], 0)
            self.next_move_weights[1] += max(other[0], 0)
            self.next_move_weights[2] += max(-1 * other[1], 0)
            self.next_move_weights[3] += max(-1 * other[0], 0)

    def do_move(self):
        # check energy
        if 0 >= self.energy:
            self.energy = randint(8, 12)
            self.timeout = 2
        
        # check timeout
        if 0 < self.timeout:
            self.timeout -= 1
            return
        
        # move
        super().do_move()
        self.energy -= 1
        
        # any neighbours that are runners are killed
        for n in self.model.grid.get_neighbors(self.pos, moore=True, include_center=True):
            if n.type == "Runner":
                n.kill()
                self.timeout = 4