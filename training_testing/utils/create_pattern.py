import random
import numpy as np
import pandas as pd
from config.config_training import *
from utils.visualization import *


def create_act_obj_pattern(nb_pattern, size_pattern, seed=42):
    print("#################")
    print("CREATING PATTERN:")
    print("seed: "+str(seed))
    print("#################")

    # Set a fixed seed for reproducibility
    random.seed(seed)

    motor = []
    visu = []
    audi = []
    arti = []
    neuron_pool_motor = set(range(0, EXC_NEURONS*EXC_NEURONS))
    neuron_pool_visu = set(range(0, EXC_NEURONS*EXC_NEURONS))
    neuron_pool_audi = set(range(0, EXC_NEURONS*EXC_NEURONS))
    neuron_pool_arti = set(range(0, EXC_NEURONS*EXC_NEURONS))

    for i in range(nb_pattern):
        motor.append(sorted(random.sample(list(neuron_pool_motor), size_pattern)))
        visu.append(sorted(random.sample(list(neuron_pool_visu), size_pattern)))
        audi.append(sorted(random.sample(list(neuron_pool_audi), size_pattern)))
        arti.append(sorted(random.sample(list(neuron_pool_arti), size_pattern)))

        neuron_pool_motor -= set(motor[-1])
        neuron_pool_visu -= set(visu[-1])
        neuron_pool_audi -= set(audi[-1])
        neuron_pool_arti -= set(arti[-1])
        
    print("✅ Step 3: Calling `show_owerlapp_pattern()`")
    show_owerlapp_pattern(motor, visu, audi, arti)
    
    print("✅ Step 4: Calling 'plot_pattern_presence()'")
    plot_pattern_presence(motor, EXC_NEURONS, "motor_patterns")
    plot_pattern_presence(visu, EXC_NEURONS, "visu_patterns")
    plot_pattern_presence(audi, EXC_NEURONS, "audi_patterns")
    plot_pattern_presence(arti, EXC_NEURONS, "arti_patterns")
    
    print("✅ Step 4: Returning patterns")

    return motor, visu, audi, arti
