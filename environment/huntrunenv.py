import time
import mesa
import yaml
import critters

class HunterRunnerEnvironment(mesa.Model):

    def __init__(self, delay, hunters_filename, runners_filename, obstacles_filename):
        super().__init__()
        self.grid = mesa.space.MultiGrid(20, 40, False)
        # self.grid = mesa.space.SingleGrid(20, 40, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.hunters = make_hunters(hunters_filename, self)
        self.runners = make_runners(runners_filename, self)
        self.obstacles = make_obstacles(obstacles_filename, self)
        self.delay = delay / 1000
        self.stopped = False

        for h in self.hunters:
            self.schedule.add(h)
            self.grid.place_agent(h, (h.initial_x, h.initial_y))
        for r in self.runners:
            self.schedule.add(r)
            self.grid.place_agent(r, (r.initial_x, r.initial_y))
        for o in self.obstacles:
            self.schedule.add(o)
            self.grid.place_agent(o, (o.initial_x, o.initial_y))

    def print_me(self):
        for a in self.schedule.agents:
            a.print_me()

    def step(self):
        escaped_count = 0
        death_count = 0
        for r in self.runners:
            if r.escaped:
                escaped_count += 1
            elif not r.alive:
                death_count += 1
        if (escaped_count + death_count) != len(self.runners):
            self.schedule.step()
            time.sleep(self.delay)
        else:
            if not self.stopped:
                print(str(escaped_count) + " escaped!")
                self.stopped = True


def make_obstacles(filename, model):
    # read parameters from file
    with open(filename, 'r') as file:
        params_dict = yaml.safe_load(file)

    n = 6
    expected_keys = []
    for i in range(n):
        expected_keys.append("x"+str(i))
        expected_keys.append("y"+str(i))

    assert set(params_dict.keys()) == set(expected_keys), "Problem with obstacles yaml file!"

    obstacles = []
    for i in range(n):
        obstacles.append(critters.Obstacle("o"+str(i), model, params_dict["x" + str(i)], params_dict["y" + str(i)]))

    return obstacles


def make_hunters(filename, model):
    # read parameters from file
    with open(filename, 'r') as file:
        params_dict = yaml.safe_load(file)

    n = 4
    expected_keys = []
    for i in range(n):
        expected_keys.append("x"+str(i))
        expected_keys.append("y"+str(i))

    assert set(params_dict.keys()) == set(expected_keys), "Problem with hunters yaml file!"

    hunters = []
    for i in range(n):
        hunters.append(critters.Hunter("h"+str(i), model, params_dict["x" + str(i)], params_dict["y" + str(i)]))

    return hunters


def make_runners(filename, model):
    # read parameters from file
    with open(filename, 'r') as file:
        params_dict = yaml.safe_load(file)

    n = 6
    expected_keys = []
    for i in range(n):
        expected_keys.append("x"+str(i))
        expected_keys.append("y"+str(i))
        expected_keys.append("p"+str(i))

    assert set(params_dict.keys()) == set(expected_keys), "Problem with runners yaml file!"

    runners = []
    for i in range(n):
        runners.append(critters.Runner("h"+str(i), model, params_dict["x" + str(i)], params_dict["y" + str(i)], params_dict["p" + str(i)]))
        
    return runners