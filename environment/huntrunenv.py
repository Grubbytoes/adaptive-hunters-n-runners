import time
import mesa

from itertools import chain

from .agentgenerator import AgentGenerator

global_environment_size = 32

class HunterRunnerEnvironment(mesa.Model):

    def __init__(self, delay=10, parent_runners=[], reproduction_type = 0, generation_id="unknown generation"):
        super().__init__()
        
        width = global_environment_size * 8
        height = int(width / 1.8)
        
        self.grid = mesa.space.MultiGrid(width, height, False)
        self.schedule = mesa.time.RandomActivation(self)
        self.delay = delay / 1000
        self.stopped = False
        self.generator = AgentGenerator(width, height, self, generation_id)       
        self.reproduction_type = reproduction_type
        
        self.hunters = []
        self.runners = []
        self.obstacles = []
        
        self.survivors = []
    
    # MUST be called before the model is run if you want to have any actual agents...!
    def populate(self, parents=[], reproduction_type=0):
        self.generator.populate(parents, reproduction_type)

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
        print(f"{len(self.survivors)} survivors")
        
        self.stopped = True
        

def get_environment_size():
    return global_environment_size


def set_environment_size(s):
    global global_environment_size
    global_environment_size = s


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