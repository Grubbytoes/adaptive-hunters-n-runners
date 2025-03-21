
import critters
import datalog
# import pygame

import environment as env


results_file = open("results.json", "w")


# run model once, with specified noise area and probability
def run():

    env.set_environment_size(50)

    LIFETIME = 128 + int(env.get_environment_size() * 16)
    GENS = 100
    REPRODUCTION_TYPE = 1
    
    model: env.HunterRunnerEnvironment = env.HunterRunnerEnvironment(generation_id="generation_0")
    critters.set_mutation_params(0.4, 0.2)
    model.populate()
    parent_generation = []
    
    iter_log = datalog.IterationLogger()
    iter_log.set_param_data((0.2, 0.2, REPRODUCTION_TYPE))
    
    for g in range (GENS):
        print(f"GENERATION {g}")
        dud_generation = False
        pop_log = datalog.PopulationLogger()
        
        # run for this number of simulation steps at maximum
        for i in range(LIFETIME):
            # step the model
            model.step()
            # draw the model
            # draw_model(model, surface)
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


def draw_model(model: env.HunterRunnerEnvironment, surface, xoff=0, yoff=0, scale=4):
    raise NotImplementedError("This version of hunter and runners no longer uses pygame, I'm afraid...")


run()
