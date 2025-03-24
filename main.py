
import critters
import datalog
import time
import itertools
import threading
# import pygame

import environment as env


RESULTS_PATH = "results/"
LIFETIME = 128 + int(env.get_environment_size() * 24)
GENS = 100
env.set_environment_size(60)

def main():
    timer = time.time()
    
    sweep_params = [p / 10 for p in range(1, 6)]
    print(sweep_params)
    
    asexual_sweep = threading.Thread(target=sweep, args=(1, sweep_params, sweep_params))
    sexual_sweep = threading.Thread(target=sweep, args=(2, sweep_params, sweep_params))

    asexual_sweep.start()
    sexual_sweep.start()

    asexual_sweep.join()
    sexual_sweep.join()

    timer = time.time() - timer
    print(f"program time: {timer} seconds")

# run model once, with specified noise area and probability
def run_with(generations=1, reproduction_type = 1, mutation_factor=0.2, mutation_strength=0.2, do_write_results=True):

    model: env.HunterRunnerEnvironment = env.HunterRunnerEnvironment(generation_id="generation_0")
    critters.set_mutation_params(mutation_factor, mutation_strength)
    model.populate()
    parent_generation = []

    iter_log = datalog.IterationLogger()
    param_data = (mutation_factor, mutation_strength, reproduction_type)
    iter_log.set_param_data(param_data)
    g = 0

    while g < generations:
        print(f"{param_data} GENERATION {g}")
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
        if reproduction_type <= len(model.survivors):
            g += 1
            parent_generation = model.survivors.copy()
        else:
            dud_generation = True
            print(f"{param_data} restarting")

        model = env.HunterRunnerEnvironment(generation_id=f"generation_{g}")

        if g == 0 and dud_generation:
            # print("Forced to restart first generation")
            model.populate()
        elif dud_generation:
            # print(f"Forced to restart generation {g}")
            model.populate(parent_generation, reproduction_type)
        else:
            model.populate(parent_generation, reproduction_type)

        # Reading th population for logging purposes
        pop_log.read(model.runners)
        iter_log.read(pop_log)

        # print("\n---\n")

    # end model if it hasn't stopped already
    model.end()

    # write the results
    if not do_write_results:
        return

    results_file_name: str
    if reproduction_type == 1:
        results_file_name = f"asexual{[mutation_factor, mutation_strength]}"
    elif reproduction_type == 2:
        results_file_name = f"sexual{[mutation_factor, mutation_strength]}"
    else:
        results_file_name = "unknown"
    write_results(iter_log, results_file_name)


def write_results(log: datalog.IterationLogger, filename:str):
    results_file = open(f"{RESULTS_PATH}{filename}.json", "w")
    results_file.write(log.dump())


def sweep(reproduction_type = 1, mutation_factor_range=[], mutation_strength_range=[], parallels=1):
    if 0 > parallels:
        raise ValueError("Cannot run negative number of threads in parallel")

    threads = []

    for f, s in itertools.product(mutation_factor_range, mutation_strength_range):
        new_thread = threading.Thread(target=run_with, args=(GENS, reproduction_type, f, s))
        threads.append(new_thread)

    for i in range(len(threads)):
        if i > parallels:
            threads[i-parallels-1].join()
        threads[i].start()

    for remaining_thread in threads[-parallels:]:
        remaining_thread.join
    
    print("SWEEP DONE!!")


def draw_model(model: env.HunterRunnerEnvironment, surface, xoff=0, yoff=0, scale=4):
    raise NotImplementedError("This version of hunter and runners no longer uses pygame, I'm afraid...")


### MAIN ###

main()
