import critters

class AgentGenerator:
    
    def __init__(self, width, height):
        self._width = width
        self._height = height
        
        self.hunters = []
        self.runners = []
        self.obstacles = []
    
    def populate(self, environmentModel):
        # TODO actually make the damn critters!
        
        for h in self.hunters:
            environmentModel.hunters.append(h)
            environmentModel.schedule.add(h)
            environmentModel.grid.place_agent(h, (h.initial_x, h.initial_y))
        for r in self.runners:
            environmentModel.runners.append(r)
            environmentModel.schedule.add(r)
            environmentModel.grid.place_agent(r, (r.initial_x, r.initial_y))
        for o in self.obstacles:
            environmentModel.obstacles.append(o)
            environmentModel.schedule.add(o)
            environmentModel.grid.place_agent(o, (o.initial_x, o.initial_y))