import pygame

import critters
import environment as env


# run model once, with specified noise area and probability
def run():

    SCALE = 4
    WIDTH = env.ENVIRONMENT_SIZE * 8 # width and height need to match those of the HuntNRun grid
    HEIGHT = int(WIDTH / 1.8)
    LIFETIME = 2
    
    XOFF = SCALE * 10 * 0 # these can be used to place an empty border around the grid
    YOFF = SCALE * 10 * 0 # - this part of the code is copied from a different application, and zeroed as not needed here
    
    # set up pygame window
    pygame.init()
    display = (SCALE*WIDTH, SCALE*HEIGHT)
    surface = pygame.display.set_mode(display)

    # set up model
    # - delay parameter can be used to control speed of animation
    #   make it small to make simulation fast
    model: env.HunterRunnerEnvironment = env.HunterRunnerEnvironment(delay=25)
    
    # Call the model to populate itself
    model.initial_populate()

    while model.generation < model.run_for:
        for i in range(LIFETIME): # run for this number of simulation steps at maximum
            draw_model_step(model, surface)
            # break out of for loop when all runners have either escaped or died
            if model.stopped:
                break
        model.end()
    
    # end model if it hasn't stopped already
    model.end()

    # input("Press Enter to close...") # this prevents the pygame window from closing instantly
    pygame.quit()
    

def draw_model_step(model: env.HunterRunnerEnvironment, surface: pygame.Surface, xoff=0, yoff=0, scale=4):
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
        pygame.draw.rect(surface, colour, pygame.Rect(xoff + col*scale, yoff + row*scale, scale, scale))

    # draw runners
    for a in model.get_agents_of_type(critters.Runner): 
        if a.alive:
            colour = (0, 0, 255)
        else:
            colour = (60, 60, 60)
        col = a.pos[0]
        row = a.pos[1]
        pygame.draw.rect(surface, colour, pygame.Rect(xoff + col*scale, yoff + row*scale, scale, scale))
    
    # draw obstacles
    for a in model.get_agents_of_type(critters.Obstacle): 
        colour = (0, 255, 0)
        col = a.pos[0]
        row = a.pos[1]
        pygame.draw.rect(surface, colour, pygame.Rect(xoff + col*scale, yoff + row*scale, scale, scale))


    pygame.display.flip()


run()
