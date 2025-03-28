from .critter import Critter
from .runnerbrain import RunnerBrain

class Runner(Critter):
    def __init__(self, unique_id, model, x, y, pause, parents=[]):
        super().__init__(unique_id, model, x, 0, sight_range=6) # make all runners' initial y = 0, so that they have to start at the bottom
        self.type = "Runner"
        self.pause = pause
        self.steps = 0
        self.escaped = False
        self.alive = True
        self.brain = RunnerBrain(parents)
        
        # vars for logging
        self.parent_record = [p.unique_id for p in parents]

    def print_me(self):
        super().print_me()
        print("Pause:", self.pause)
    
    def decide_move(self):
        super().decide_move()
        self.brain.think(self.next_move_weights, self.vision)

    def do_move(self):
        # runners will only move if they have not escaped already
        if self.escaped:
            return
        # and they have not been killed by hunters
        elif not self.alive:
            return
        
        # if they get this far then it counts as a step
        self.steps += 1
        
        # wait if they need to
        if self.steps <= self.pause:
            return
        
        super().do_move()
        
        if self.pos[1] >= self.model.grid.height - 1:
            gene_dump = self.brain.gene_dump()
            
            self.escaped = True
            self.model.survivors.append(self)
    
    def kill(self):
        self.alive = False
        self.type = 'DeadCritter' #! not fully happy with this...!
    
    def gene_dump(self):
        return self.brain.gene_dump()