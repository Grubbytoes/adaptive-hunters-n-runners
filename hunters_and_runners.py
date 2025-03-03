import mesa
import numpy as np
import time
import yaml
import pygame
import hugo_tools as ht

'''
    Superclass for hunters and runners.
'''
class Critter(mesa.Agent):

    def __init__(self, unique_id, model, moves, x, y, sight_range = 1):
        super().__init__(unique_id, model)
        self.moves = moves
        self.move_ind = 0
        self.next_move = "R"
        self.type = "Undefined"
        self.initial_x = x
        self.initial_y = y

        # Vision
        self.sight_range = max(sight_range, 1)
        self.vision = []

    '''
        A function to print information about agents and their programs.
    '''
    def print_me(self):
        print("\nAgent, type:", self.type)
        print("Initial coords: (" + str(self.initial_x) + "," + str(self.initial_y) + ")")
        print("Move sequence:", self.moves)
        print("I can see: ", self.vision)

    def step(self):
        self.see()
        self.decide_move()
        self.do_move()
    
    def decide_move(self):
        # if end of program has been reached, loop back to beginning
        if self.move_ind > (len(self.moves)-1):
            self.move_ind = 0
        # get next move from program
        self.next_move = self.moves[self.move_ind]

    '''
        Move agent, according to its program. Agents cannot occupy the same space as an obstacle, or other agent. 
    '''
    def do_move(self):
        
        # initialise coordinates for next step to current location
        new_x = self.pos[0]
        new_y = self.pos[1]

        # set coordinates for attempted move - move may be blocked later, by obstacle or other agent
        if self.next_move == "R": # pick random location in Moore neighbourhood
            new_x = self.pos[0] + np.random.choice([-1, 0, 1])
            new_y = self.pos[1] + np.random.choice([-1, 0, 1])
        elif self.next_move == "N": # set y to row above 
            new_y = self.pos[1] + 1
        elif self.next_move == "S": # set y to row below
            new_y = self.pos[1] - 1
        elif self.next_move == "E": # set x to right column
            new_x = self.pos[0] + 1
        elif self.next_move == "W": # set x to left column
            new_x = self.pos[0] - 1
        else:
            print("Not a valid move!")

        if new_y < 0: # prevent agents from moving off bottom of grid
            new_y = 0
        elif new_y >= self.model.grid.height: # prevent agents from moving off top of grid
            new_y = self.model.grid.height - 1

        if new_x < 0: # prevent agents from moving off left of grid
            new_x = 0
        elif new_x >= self.model.grid.width: # prevent agents from moving off right of grid
            new_x = self.model.grid.width - 1

        # get obstacles and agents in Moore neighbourhood
        neighbours = self.model.grid.get_neighbors(self.pos, True)
        move = True
        for n in neighbours:
            if n.pos == (new_x, new_y): # prevent moving into cell with obstacle or other agent
                move = False    

        if move:        
            self.model.grid.move_agent(self, (new_x, new_y)) # move
            
        self.move_ind += 1 # increment program index
    
    def see(self): 
        # clear vision
        self.vision.clear()

        for other in self.model.grid.get_neighbors(self.pos, True, radius=self.sight_range):
            thing_entry = (
                int(other.pos[0] - self.pos[0]),
                int(other.pos[1] - self.pos[1]),
                other.type
            )
            self.vision.append(thing_entry)

class Hunter(Critter):
    def __init__(self, unique_id, model, moves, x, y):
        super().__init__(unique_id, model, moves, x, max(30, y), sight_range=3) # make all hunters start near the top of the environment
        self.type = "Hunter"

    def do_move(self):
        # move
        super().do_move()

        # get neighbours
        neighbours = self.model.grid.get_neighbors(self.pos,
                                                    moore=True,
                                                    include_center=True)
        
        # any neighbours that are runners are killed
        for n in neighbours:
            if n.type == "Runner":
                n.alive = False  

class Runner(Critter):
    def __init__(self, unique_id, model, moves, x, y, pause):
        super().__init__(unique_id, model, moves, x, 0, sight_range=4) # make all runners' initial y = 0, so that they have to start at the bottom
        self.type = "Runner"
        self.pause = pause
        self.steps = 0
        self.escaped = False
        self.alive = True

    def print_me(self):
        super().print_me()
        print("Pause:", self.pause)

    def do_move(self):
        # runners will only move if they have not escaped already, and they have not been killed by hunters
        if not self.escaped and self.alive:
            if self.steps < self.pause:
                self.steps += 1
            else:
                super().do_move()
                if self.pos[1] >= self.model.grid.height - 1:
                    self.escaped = True

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
        obstacles.append(Obstacle("o"+str(i), model, params_dict["x" + str(i)], params_dict["y" + str(i)]))

    return obstacles

def make_hunters(filename, model):
    # read parameters from file
    with open(filename, 'r') as file:
        params_dict = yaml.safe_load(file)

    n = 4
    expected_keys = ["movelist"]
    for i in range(n):
        expected_keys.append("x"+str(i))
        expected_keys.append("y"+str(i))

    assert set(params_dict.keys()) == set(expected_keys), "Problem with hunters yaml file!"

    hunters = []
    for i in range(n):
        hunters.append(Hunter("h"+str(i), model, params_dict["movelist"], params_dict["x" + str(i)], params_dict["y" + str(i)]))

    return hunters

def make_runners(filename, model):
    # read parameters from file
    with open(filename, 'r') as file:
        params_dict = yaml.safe_load(file)

    n = 6
    expected_keys = ["movelist"]
    for i in range(n):
        expected_keys.append("x"+str(i))
        expected_keys.append("y"+str(i))
        expected_keys.append("p"+str(i))

    assert set(params_dict.keys()) == set(expected_keys), "Problem with runners yaml file!"

    runners = []
    for i in range(n):
        runners.append(Runner("h"+str(i), model, params_dict["movelist"], params_dict["x" + str(i)], params_dict["y" + str(i)], params_dict["p" + str(i)]))
        
    return runners

# run model once, with specified noise area and probability
def run():

    SCALE = 4
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
    model = HuntNRun(delay=150, hunters_filename="hunters.yaml", runners_filename="runners.yaml", obstacles_filename="obstacles.yaml")

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
        for a in model.get_agents_of_type(Hunter): 
            colour = (255, 0, 0)
            col = a.pos[0]
            row = a.pos[1]
            pygame.draw.rect(surface, colour, pygame.Rect(XOFF + col*SCALE, YOFF + row*SCALE, SCALE, SCALE))

        # draw runners
        for a in model.get_agents_of_type(Runner): 
            if a.alive:
                colour = (0, 0, 255)
            else:
                colour = (60, 60, 60)
            col = a.pos[0]
            row = a.pos[1]
            pygame.draw.rect(surface, colour, pygame.Rect(XOFF + col*SCALE, YOFF + row*SCALE, SCALE, SCALE))
        
        # draw obstacles
        for a in model.get_agents_of_type(Obstacle): 
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

