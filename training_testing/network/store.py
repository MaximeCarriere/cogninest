# store.py
import pickle
import pandas as pd
from tqdm import tqdm
import nest
from utils.file_operations import ensure_directory_exists

def store(self, filename, motor, visu, audi, arti):
    """
    Store neuron membrane potential and synaptic weights to given file with a progress bar.
    """
    print("\n💾 SAVING NETWORK ==> ", filename)
    assert nest.NumProcesses() == 1, "Cannot dump MPI parallel"

    ## 🟢 Inhibitory Parameters
    print("\n🔹 Extracting Inhibitory Parameters...")
    inh_neurons_param_list = ["k_1", "tau_m"]
    list_param_value_inh = []
    for param in tqdm(inh_neurons_param_list, desc="Processing Inhibitory Parameters"):
        value = list(set(self.areas['A1'].inh.get([param], output="pandas")[param].values.tolist()))
        list_param_value_inh.append([param, value])
    list_param_value_inh = pd.DataFrame(list_param_value_inh, columns=["param", "value"])

    ## 🟢 Excitatory Parameters
    print("\n🔹 Extracting Excitatory Parameters...")
    exc_neurons_param_list = ["om", "alpha", "alpha_e", "tau_adapt", "k_2", "Jexcitatory", "tau_m"]
    list_param_value = []
    for param in tqdm(exc_neurons_param_list, desc="Processing Excitatory Parameters"):
        value = list(set(self.areas['A1'].exc.get([param], output="pandas")[param].values.tolist()))
        list_param_value.append([param, value])
    list_param_value = pd.DataFrame(list_param_value, columns=["param", "value"])

    ## 🟢 Global Inhibition Parameters
    print("\n🔹 Extracting Global Inhibition Parameters...")
    glob_neurons_param_list = ["k_1", "tau_m"]
    list_param_value_glob = []
    for param in tqdm(glob_neurons_param_list, desc="Processing Global Inhibition Parameters"):
        value = list(set(self.areas['A1'].glob.get([param], output="pandas")[param].values.tolist()))
        list_param_value_glob.append([param, value])
    list_param_value_glob = pd.DataFrame(list_param_value_glob, columns=["param", "value"])

    ## 🟢 Store Neurons Data
    print("\n🔹 Extracting Neuron Data...")

    excitatory_neurons = []
    inhibitory_neurons = []
    global_inhibition = []

    for area in tqdm(self.areas.keys(), desc="Processing Areas"):
        eph = self.areas[area].exc.get(output="pandas")
        eph["area"] = area
        excitatory_neurons.append(eph)

        eph_i = self.areas[area].inh.get(output="pandas")
        eph_i["area"] = area
        inhibitory_neurons.append(eph_i)

        eph_g = self.areas[area].glob.get(output="pandas")
        eph_g["area"] = area
        global_inhibition.append(eph_g)

    excitatory_neurons = pd.concat(excitatory_neurons)
    inhibitory_neurons = pd.concat(inhibitory_neurons)
    global_inhibition = pd.concat(global_inhibition)

    ## 🟢 Store Synaptic Weights
    print("\n🔹 Extracting Synaptic Weights...")
    test = nest.GetConnections().get(
        ("delay", "receptor", "source", "synapse_model", "target", "weight"), output="pandas"
    )

    ## 🟢 Save Network Data
    network = {
        "param_excitatory": list_param_value,
        "param_inhibitory": list_param_value_inh,
        "param_global": list_param_value_glob,
        "weight": test,
        "pattern_motor": motor,
        "pattern_visual": visu,
        "pattern_auditory": audi,
        "pattern_articulatory": arti,
        "excitatory_neurons": excitatory_neurons,
        "inhibitory_neurons": inhibitory_neurons,
        "global_inhibition": global_inhibition,
    }

    directory = "./save_network/"
    ensure_directory_exists(directory)

    with open(directory + filename, "wb") as f:
        pickle.dump(network, f, pickle.HIGHEST_PROTOCOL)

    print("✅ Saving Complete!")
