import time
import nest
import sys
import os
# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Only install if it's not already loaded
installed_modules = nest.GetKernelStatus().get("loaded_modules", [])
if "felixmodule" not in installed_modules:
    nest.Install('felixmodule')
else:
    print("Felix Module is already installed, skipping installation.")

from network.network_building import FelixNet
from utils.file_operations import *
from utils.visualization import *
from utils.create_pattern import *

from config.config_training import TOTAL_TRAINING, NB_PATTERN, SIZE_PATTERN, SEED, stim_strength


if __name__ == "__main__":
    tic = time.time()
    f = FelixNet()
    f.build_net()
    toc = time.time()
    
    ensure_directory_exists("./plot_training")
    print(f"Build Time: {toc-tic:.1f} s")

    motor, visu, audi, arti = create_act_obj_pattern(NB_PATTERN, SIZE_PATTERN, SEED)
    
    tic = time.time()
    f.train_action_object(motor, visu, audi, arti, num_reps=TOTAL_TRAINING, stim_strength=stim_strength, nb_pattern=NB_PATTERN)


    toc = time.time()
    print(f"Train Time: {toc-tic:.1f} s")
