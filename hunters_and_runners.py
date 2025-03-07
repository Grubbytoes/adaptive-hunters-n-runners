import mesa
import time
import yaml
import pygame
import critters

class HuntNRun(mesa.Model):

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


# run model once, with specified noise area and probability
def run():

    SCALE = 8
    WIDTH = 20 # width and height need to match those of the HuntNRun grid
    HEIGHT = 40
    XOFF = SCALE * 10 * 0 # these can be used to place an empty border around the grid
    YOFF = SCALE * 10 * 0 # - this part of the code is copied from a different application, and zeroed as not needed here
    
    # set up pygame window
    pygame.init()
    display = (SCALE*WIDTH, SCALE*HEIGHT)
    surface = pygame.display.set_mode(display)

    # set up model
    # - delay parameter can be used to control speed of animation
    #   make it small to make simulation fast
    model = HuntNRun(delay=75, hunters_filename="hunters.yaml", runners_filename="runners.yaml", obstacles_filename="obstacles.yaml")

    for i in range(10000): # run for this number of simulation steps at maximum
        # step the model
        model.step()

        # if pygame window is closed, then quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # fill pygame window background in black
        surface.fill((0, 0, 0))

        # draw hunters
        for a in model.get_agents_of_type(critters.Hunter): 
            colour = (255, 0, 0)
            col = a.pos[0]
            row = a.pos[1]
            pygame.draw.rect(surface, colour, pygame.Rect(XOFF + col*SCALE, YOFF + row*SCALE, SCALE, SCALE))

        # draw runners
        for a in model.get_agents_of_type(critters.Runner): 
            if a.alive:
                colour = (0, 0, 255)
            else:
                colour = (60, 60, 60)
            col = a.pos[0]
            row = a.pos[1]
            pygame.draw.rect(surface, colour, pygame.Rect(XOFF + col*SCALE, YOFF + row*SCALE, SCALE, SCALE))
        
        # draw obstacles
        for a in model.get_agents_of_type(critters.Obstacle): 
            colour = (0, 255, 0)
            col = a.pos[0]
            row = a.pos[1]
            pygame.draw.rect(surface, colour, pygame.Rect(XOFF + col*SCALE, YOFF + row*SCALE, SCALE, SCALE))


        pygame.display.flip()
        pygame.time.wait(0) # wait for specified number of ms - not really needed, as model has built in delay

        # break out of for loop when all runners have either escaped or died
        if model.stopped:
            break

    # input("Press Enter to close...") # this prevents the pygame window from closing instantly
    pygame.quit()

run()

