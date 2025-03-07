import mesa

class Obstacle(mesa.Agent):
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.type = "Obstacle"
        self.initial_x = x
        self.initial_y = y
    
    def print_me(self):
        print("\nAgent, type:", self.type)
        print("Initial coords: (" + str(self.initial_x) + "," + str(self.initial_y) + ")")

    def step(self):
        pass