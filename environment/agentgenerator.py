import critters
import random

random.seed()

class AgentGenerator:
    
    def __init__(self, width, height):
        
        self._width = width
        self._height = height
        
    
    def populate(self, environment_model):
        hunters = []
        runners = []
        obstacles = []
        
        runner_count: int = int(self._width / 8)
        hunter_count: int = int(runner_count / 2) - 1
        obstacle_count: int = int(self._width * self._height * 0.5 * 0.05)
        forest_band = (
            int(self._height / 8), 
            int(self._height / 8 * 7)
        )
        
        # making runners
        for i in range(runner_count):
            x_position = random.randint(0, 7) + 8 * i
            new_runner = critters.Runner(f"r{i}", environment_model, x_position, 0, random.randint(0, 8))
            runners.append(new_runner)
            
        # making hunters
        for i in range(hunter_count):
            x_position = random.randint(0, 15) + 16 * i
            y_position = random.randint(*forest_band)
            new_hunter = critters.Hunter(f"h{i}", environment_model, x_position, y_position)
            hunters.append(new_hunter)
            
        # making obstacles
        for i in range(obstacle_count):
            # find a space
            x_position = random.randint(0, self._width)
            y_position = random.randint(*forest_band)
            while (x_position, y_position) not in environment_model.grid.empties: #! eww...
                x_position = random.randint(0, self._width)
                y_position = random.randint(*forest_band)
            new_obstacle = critters.Obstacle(f"o{i}", environment_model, x_position, y_position)
            obstacles.append(new_obstacle)
            
        
        for h in hunters:
            environment_model.hunters.append(h)
            environment_model.schedule.add(h)
            environment_model.grid.place_agent(h, (h.initial_x, h.initial_y))
        for r in runners:
            environment_model.runners.append(r)
            environment_model.schedule.add(r)
            environment_model.grid.place_agent(r, (r.initial_x, r.initial_y))
        for o in obstacles:
            environment_model.obstacles.append(o)
            environment_model.schedule.add(o)
            environment_model.grid.place_agent(o, (o.initial_x, o.initial_y))