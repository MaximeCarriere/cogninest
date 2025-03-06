# train_action_object.py
import random
import nest
from utils.stim import stim_specs_patt_no, stim_specs_patt_no_testing_audi_only, stim_specs_patt_no_testing_arti_only
from utils.visualization import save_plot_activation_new
from utils.file_operations import ensure_directory_exists
from utils.gathering import *
from config.config_training import verbose, when_to_save, when_to_plot
import numpy as np
from tqdm import tqdm
import pandas as pd

def train_action_object(self, motor, visu, audi, arti, num_reps=10, t_on=16, t_off=30, stim_specs=None, nb_pattern=2, stim_strength=500):
    ensure_directory_exists("./save_network")
    ensure_directory_exists("./processing_data", clear=True)

    nest.SetKernelStatus({'overwrite_files': True, 'data_path': "./processing_data"})
    patt_no = 0
    if 0 in when_to_save:
        self.store("network_0", motor, visu, audi, arti)
    gi_tot = []
    patt_no_count = [0] * nb_pattern
    count_firs_pres = 0

    while any(count < num_reps for count in patt_no_count):
        with nest.RunManager():
            patt_no = random.randint(0, nb_pattern - 1)
            if patt_no_count[patt_no] >= num_reps:
                continue

            print(f"################\nPresentation patt_no: {patt_no}")
            nest.SetKernelStatus({'overwrite_files': True})

            stim_specs = stim_specs_patt_no(self, patt_no, nb_pattern, motor, visu, audi, arti, stim_strength)
            patt_no_count[patt_no] += 1

            self.stimulation_on(stim_specs)
            for _ in range(t_on):
                nest.Run(0.5)
            self.stimulation_off()

            ## Wait until the GI goes below a given threshold
            counter_stim_pause = 0
            self.stimulation_off()
            gi_PB = self.areas["PB"].glob.get(output="pandas")["V_m"].values[0]
            gi_PF_i = self.areas["PF_i"].glob.get(output="pandas")["V_m"].values[0]
            while ((gi_PB > 0.70) | (gi_PF_i > 0.70) | (counter_stim_pause < t_off)):
                    nest.Run(0.5)
                    gi_PB = self.areas["PB"].glob.get(output="pandas")["V_m"].values[0]
                    gi_PF_i = self.areas["PF_i"].glob.get(output="pandas")["V_m"].values[0]
                    counter_stim_pause += 0.5

            # Save progress every 30 presentations
            if np.sum(patt_no_count) % when_to_plot == 0:
                dat = dat_from_file('./processing_data/felix-*.dat')
                dat['sum'] = dat['matrix'].apply(sum_arrays)
                dat["Pres"] = patt_no_count[patt_no]
                dat["patt_no"] = patt_no
                save_plot_activation_new(patt_no_count[patt_no], dat, patt_no)

            # Save network at specific intervals
            if (patt_no_count[-1] in when_to_save) and (patt_no == nb_pattern - 1) and (patt_no_count[-1]!=0):
                self.store(f"network_{patt_no_count[-1]}", motor, visu, audi, arti)

    save_plot_weight(self, patt_no_count[-1])
    dat['sum'] = dat['matrix'].apply(sum_arrays)
    save_plot_activation_new(patt_no_count[-1], dat, patt_no)
