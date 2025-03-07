from .critter import Critter


class Runner(Critter):
    def __init__(self, unique_id, model, x, y, pause):
        super().__init__(unique_id, model, x, 0, sight_range=4) # make all runners' initial y = 0, so that they have to start at the bottom
        self.type = "Runner"
        self.pause = pause
        self.steps = 0
        self.escaped = False
        self.alive = True

    def print_me(self):
        super().print_me()
        print("Pause:", self.pause)
    
    def decide_move(self):
        super().decide_move()
        self.next_move_weights[0] += 0.1


    def do_move(self):
        # runners will only move if they have not escaped already, and they have not been killed by hunters
        if not self.escaped and self.alive:
            if self.steps < self.pause:
                self.steps += 1
            else:
                super().do_move()
                if self.pos[1] >= self.model.grid.height - 1:
                    self.escaped = True
    
    def kill(self):
        self.alive = False
        self.type = 'DeadCritter' #! not fully happy with this...!