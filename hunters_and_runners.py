import pygame

import critters
import datalog
import environment as env


results_file = open("results.json", "w")


# run model once, with specified noise area and probability
def run():

    env.set_environment_size(50)

    SCALE = 4 # TODO wtf...!?
    WIDTH = env.get_environment_size() * 8 # width and height need to match those of the HuntNRun grid
    HEIGHT = int(WIDTH / 1.8)
    LIFETIME = 128 + int(env.get_environment_size() * 16)
    GENS = 10
    REPRODUCTION_TYPE = 1

    # set up pygame window
    pygame.init()
    display = (SCALE*WIDTH, SCALE*HEIGHT)
    surface = pygame.display.set_mode(display)
    
    model: env.HunterRunnerEnvironment = env.HunterRunnerEnvironment(generation_id="generation_0")
    critters.set_mutation_params(0.4, 0.2)
    model.populate()
    parent_generation = []
    
    iter_log = datalog.IterationLogger()
    for g in range (GENS):
        print(f"GENERATION {g}")
        dud_generation = False
        pop_log = datalog.PopulationLogger()
        
        # run for this number of simulation steps at maximum
        for i in range(LIFETIME):
            draw_model_step(model, surface)
            # break out of for loop when all runners have either escaped or died
            if model.stopped:
                break
        model.end()

        # get survivors, otherwise try again
        if REPRODUCTION_TYPE <= len(model.survivors):
            g += 1
            parent_generation = model.survivors
        else:
            dud_generation = True

        model = env.HunterRunnerEnvironment(generation_id=f"generation_{g}")

        if dud_generation and len(parent_generation) < REPRODUCTION_TYPE:
            print("Forced to restart first generation")
            model.populate()
        elif dud_generation:
            print(f"Forced to restart generation {g}")
            model.populate(parent_generation, REPRODUCTION_TYPE)
        else:
            model.populate(parent_generation, REPRODUCTION_TYPE)
        
        # Reading th population for logging purposes
        pop_log.read(model.runners)
        iter_log.read(pop_log)
        
        print("\n---\n")

    # end model if it hasn't stopped already
    model.end()
    
    # write the iteration log
    results_file.write(iter_log.dump())

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
