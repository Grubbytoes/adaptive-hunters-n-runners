from .critter import Critter


class Hunter(Critter):
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model, x, max(30, y), sight_range=8) # make all hunters start near the top of the environment
        self.type = "Hunter"

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
        # move
        super().do_move()
        
        # any neighbours that are runners are killed
        for n in self.model.grid.get_neighbors(self.pos, moore=True, include_center=True):
            if n.type == "Runner":
                n.kill()