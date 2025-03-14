import pygame

import critters
import environment as env


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
    model = env.HunterRunnerEnvironment(delay=75, hunters_filename="hunters.yaml", runners_filename="runners.yaml", obstacles_filename="obstacles.yaml")

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

