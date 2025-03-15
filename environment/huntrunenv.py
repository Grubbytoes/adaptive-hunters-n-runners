import time
import mesa

from .agentgenerator import AgentGenerator

class HunterRunnerEnvironment(mesa.Model):

    def __init__(self, delay):
        super().__init__()
        
        width = 160
        height = 144
        
        self.grid = mesa.space.MultiGrid(width, height, False)
        self.schedule = mesa.time.RandomActivation(self)
        self.delay = delay / 1000
        self.stopped = False
        self.generator = AgentGenerator(width, height, self)
        
        self.hunters = []
        self.runners = []
        self.obstacles = []
        
        self.survivors = []
    
    # MUST be called before the model is run if you want to have any actual agents...!
    def populate(self):
        self.generator.populate()
    
    def populate_next_generation(self, parents):
        pass
        # TODO

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
            self.end()
    
    def end(self):
        if self.stopped:
            return

        print("Game over, man!")
        self.stopped = True


# def make_obstacles(filename, model):
#     # read parameters from file
#     with open(filename, 'r') as file:
#         params_dict = yaml.safe_load(file)

#     n = 6
#     expected_keys = []
#     for i in range(n):
#         expected_keys.append("x"+str(i))
#         expected_keys.append("y"+str(i))

#     assert set(params_dict.keys()) == set(expected_keys), "Problem with obstacles yaml file!"

#     obstacles = []
#     for i in range(n):
#         obstacles.append(critters.Obstacle("o"+str(i), model, params_dict["x" + str(i)], params_dict["y" + str(i)]))

#     return obstacles


# def make_hunters(filename, model):
#     # read parameters from file
#     with open(filename, 'r') as file:
#         params_dict = yaml.safe_load(file)

#     n = 4
#     expected_keys = []
#     for i in range(n):
#         expected_keys.append("x"+str(i))
#         expected_keys.append("y"+str(i))

#     assert set(params_dict.keys()) == set(expected_keys), "Problem with hunters yaml file!"

#     hunters = []
#     for i in range(n):
        # hunters.append(critters.Hunter("h"+str(i), model, params_dict["x" + str(i)], params_dict["y" + str(i)]))

#     return hunters


# def make_runners(filename, model):
#     # read parameters from file
#     with open(filename, 'r') as file:
#         params_dict = yaml.safe_load(file)

#     n = 6
#     expected_keys = []
#     for i in range(n):
#         expected_keys.append("x"+str(i))
#         expected_keys.append("y"+str(i))
#         expected_keys.append("p"+str(i))

#     assert set(params_dict.keys()) == set(expected_keys), "Problem with runners yaml file!"

#     runners = []
#     for i in range(n):
#         runners.append(critters.Runner("h"+str(i), model, params_dict["x" + str(i)], params_dict["y" + str(i)], params_dict["p" + str(i)]))
        
#     return runners