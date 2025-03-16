import critters
import random

random.seed()

class AgentGenerator:

    def __init__(self, width, height, model):

        self._width = width
        self._height = height
        self._model = model
        self._reserved_parents = []

    def populate(self, parent_runners=[], ignore_dud=False, reproduction_type=0):
        # checking if this is a dud generation
        # if it is we repopulate using the grandparents
        if len(parent_runners) == 0 and not ignore_dud:
            self._model.dud_generations += 1
            parent_runners = self._reserved_parents
        elif 0 < len(parent_runners):
            self._reserved_parents = parent_runners # incase they're needed in the future
        
        hunters = self.populate_hunters()
        runners = self.populate_runners(parent_runners, reproduction_type)
        obstacles = self.populate_obstacles()
        
        for h in hunters:
            self._model.hunters.append(h)
            self._model.schedule.add(h)
            self._model.grid.place_agent(h, (h.initial_x, h.initial_y))
        for r in runners:
            self._model.runners.append(r)
            self._model.schedule.add(r)
            self._model.grid.place_agent(r, (r.initial_x, r.initial_y))
        for o in obstacles:
            self._model.obstacles.append(o)
            self._model.schedule.add(o)
            self._model.grid.place_agent(o, (o.initial_x, o.initial_y))

    def populate_runners(self, parents=[], reproduction_type=0) -> list[critters.Critter]:
        runner_count: int = int(self._width / 8)

        if 0 >= reproduction_type:
            return self.first_gen_runners(runner_count)
        elif 1 == reproduction_type:
            return self.asexual_gen_runners(runner_count, parents)
        else: # would need to change this if we want sexual reproduction with more than 2 parents
            return self.sexual_gen_runners(runner_count, parents)

    def populate_hunters(self) -> list[critters.Critter]:
        hunters = []
        hunter_count = int(self._width / 16)
        hunter_band = (
            int(self._height / 8),
            int(self._height / 8 * 7)
        )

        # making hunters
        for i in range(hunter_count):
            x_position = random.randint(0, 15) + 16 * i
            y_position = random.randint(*hunter_band)
            new_hunter = critters.Hunter(f"generation {self._model.generation} h{i}", self._model, x_position, y_position)
            hunters.append(new_hunter)

        return hunters

    def populate_obstacles(self) -> list[critters.Critter]:
        obstacles = []
        obstacle_count: int = int(self._width * self._height * 0.5 * 0.05)
        obstacle_band = (
            int(self._height / 8),
            int(self._height / 8 * 7)
        )

        # making obstacles
        for i in range(obstacle_count):
            # find a space
            x_position = random.randint(0, self._width)
            y_position = random.randint(*obstacle_band)
            while (x_position, y_position) not in self._model.grid.empties: #! eww...
                x_position = random.randint(0, self._width)
                y_position = random.randint(*obstacle_band)
            new_obstacle = critters.Obstacle(f"generation {self._model.generation} o{i}", self._model, x_position, y_position)
            obstacles.append(new_obstacle)

        return obstacles

    def first_gen_runners(self, runner_count):
        runners = []

        for i in range(runner_count):
            x_position = random.randint(0, 7) + 8 * i
            new_runner = critters.Runner(f"generation {self._model.generation} r{i}", self._model, x_position, 0, random.randint(0, 8))
            runners.append(new_runner)

        return runners

    def asexual_gen_runners(self, runner_count, parents: critters.Runner):
        runners = []
        
        for i in range(runner_count):
            p = random.choice(parents)
            
            x_position = random.randint(0, 7) + 8 * i
            new_runner = critters.Runner(f"generation {self._model.generation} r{i}", self._model, x_position, 0, random.randint(0, 8), parents=[p])
            runners.append(new_runner)

        return runners

    def sexual_gen_runners(self, runner_count, parents: list[critters.Runner]):
        runners = []
        
        for i in range(runner_count):
            x_position = random.randint(0, 7) + 8 * i
            new_runner = critters.Runner(f"generation {self._model.generation} r{i}", self._model, x_position, 0, random.randint(0, 8))
            runners.append(new_runner)

        return runners