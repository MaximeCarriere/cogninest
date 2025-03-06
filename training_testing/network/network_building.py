# network_building.py
import nest
from collections import defaultdict
from utils.gathering import *
from utils.stim import *
from utils.visualization import *
from .area import Area
from .restore_area import Restore_Area
from tqdm import tqdm  # For a nice progress bar
from config.config_training import between_min, between_max, verbose, when_to_save
from network.store import store  # Import the store function
from network.train_action_object import train_action_object  # Import the train_action_object function
from network.testing_network import rebuild_net, reconnect_areas, test_aud, test_art, test_gui


class FelixNet:
    def __init__(self):
        print("Initializing FelixNet")

        nest.set_verbosity("M_ERROR")

        try:
            nest.ResetKernel()
            nest.set(resolution=0.5, local_num_threads=12, rng_seed=12)
        except Exception as e:
            print("Error during NEST kernel reset:", e)

    def build_net(self):
        self.areas = {area: Area(area) for area in ['V1', 'TO', 'AT', 'PF_L', 'PM_L', 'M1_L',
                                                    'A1', 'AB', 'PB', 'PF_i', 'PM_i', 'M1_i']}

        if verbose==1:
            ## 🔹 DEBUG: Print number of neurons in each area
            print("\n✅ Checking Neuron Counts in Each Area:")
            for area_name, area in self.areas.items():
                try:
                    num_exc = len(area.exc)
                    num_inh = len(area.inh)
                    num_glob = len(area.glob)
                    num_pg = len(area.pg) if hasattr(area, 'pg') else 0
                    print(f"📌 Area {area_name}: Excitatory={num_exc}, Inhibitory={num_inh}, Global={num_glob}, PG={num_pg}")
                except AttributeError as e:
                    print(f"❌ ERROR in area {area_name}: {e}")

            print("✅ All areas initialized\n")

        ## 🔹 Establish connections
        self.connect_areas()
        self.connect_recorders()

                                                
    def neurons2IDs(self, neurons):
        """
        Translates neuron numbers from 1 to 625 to their corresponding ID within an area of the model.

        neurons -- list of neuron numbers
        """
        return sorted(neurons)
        
    def stimulation_on(self, stim_specs):
        for area, specs in stim_specs.items():
            self.areas[area].stimulation_on(**specs)

    def stimulation_off(self):
        for area in self.areas.values():
            area.stimulation_off()
            





    def connect_areas(self):
        """
        Create inter-area connections and print a structured connectivity summary with actual connection counts.
        """

        # Store connection counts
        connection_counts = defaultdict(int)

        connectome = [
            # Visual System
            ('V1', 'TO'), ('V1', 'AT'), ('TO', 'AT'),
            # Motor System
            ('PF_L', 'PM_L'), ('PF_L', 'M1_L'), ('PM_L', 'M1_L'),
            # Auditory System
            ('A1', 'AB'), ('A1', 'PB'), ('AB', 'PB'),
            # Articulatory System
            ('PF_i', 'PM_i'), ('PF_i', 'M1_i'), ('PM_i', 'M1_i'),
            # Cross system next-neighbour
            ('AT', 'PF_L'), ('AT', 'PB'), ('AT', 'PF_i'),
            ('PF_L', 'PB'), ('PF_L', 'PF_i'), ('PB', 'PF_i'),
            # Cross system jumping links
            ('TO', 'PF_L'), ('AT', 'PM_L'), ('AB', 'PF_i'), ('PB', 'PM_i')
        ]

        cross_system = [
            ('AT', 'PF_L'), ('AT', 'PB'), ('AT', 'PF_i'),
            ('PF_L', 'PB'), ('PF_L', 'PF_i'), ('PB', 'PF_i'),
            ('TO', 'PF_L'), ('AT', 'PM_L'), ('AB', 'PF_i'), ('PB', 'PM_i')
        ]

        within_system = [
            ('V1', 'TO'), ('V1', 'AT'), ('TO', 'AT'),
            ('PF_L', 'PM_L'), ('PF_L', 'M1_L'), ('PM_L', 'M1_L'),
            ('A1', 'AB'), ('A1', 'PB'), ('AB', 'PB'),
            ('PF_i', 'PM_i'), ('PF_i', 'M1_i'), ('PM_i', 'M1_i')
        ]

        # If you do not want reciprocal connections, comment the next two lines
        cross_system.extend([(tgt, src) for src, tgt in cross_system])
        within_system.extend([(tgt, src) for src, tgt in within_system])

        kc_cross = 0.13 * 0.5
        kc_within = 0.13

        print("\n🔗 **Creating Inter-Area Connections...**")

        # **Cross-System Connections**
        print("\n🌐 **Cross-System Connections:**")
        for src, tgt in tqdm(cross_system, desc="Connecting Cross-System Areas"):
            nest.Connect(self.areas[src].exc, self.areas[tgt].exc,
                         {'rule': 'pairwise_bernoulli',
                          'p': kc_cross * nest.spatial_distributions.gaussian2D(nest.spatial.distance.x,
                                                                                nest.spatial.distance.y,
                                                                                std_x=9, std_y=9, mean_x=0,
                                                                                mean_y=0, rho=0),
                          'mask': {'grid': {'shape': [19, 19]}, 'anchor': [9, 9]}},
                         {'synapse_model': 'abs_synapse', 'receptor_type': 1,
                          'weight': nest.random.uniform(between_min, between_max), 'delay': 1})

        # **Within-System Connections**
        print("\n🏠 **Within-System Connections:**")
        for src, tgt in tqdm(within_system, desc="Connecting Within-System Areas"):
            nest.Connect(self.areas[src].exc, self.areas[tgt].exc,
                         {'rule': 'pairwise_bernoulli',
                          'p': kc_within * nest.spatial_distributions.gaussian2D(nest.spatial.distance.x,
                                                                                 nest.spatial.distance.y,
                                                                                 std_x=9, std_y=9, mean_x=0,
                                                                                 mean_y=0, rho=0),
                          'mask': {'grid': {'shape': [19, 19]}, 'anchor': [9, 9]}},
                         {'synapse_model': 'abs_synapse', 'receptor_type': 1,
                          'weight': nest.random.uniform(between_min, between_max), 'delay': 1})

        if verbose==1:
            # **Retrieve and Count Connections**
            print("\n📊 **Retrieving Connection Data...**")
            network_weights = nest.GetConnections().get(
                ("source", "target", "weight"), output="pandas"
            )

            
            # Compute actual number of connections per area pair
            for (src, tgt) in cross_system + within_system:
                try:
                    # ✅ Dynamically fetch excitatory neurons for each area
                    n_area1 = self.areas[src].exc.get(output="pandas")
                    n_area2 = self.areas[tgt].exc.get(output="pandas")

                    # ✅ Filter weight data to count connections from src to tgt
                    weight_data = network_weights[
                        (network_weights["source"].isin(n_area1.index)) &
                        (network_weights["target"].isin(n_area2.index))
                    ]

                    connection_counts[(src, tgt)] = len(weight_data)

                except KeyError as e:
                    print(f"⚠️ Warning: Could not fetch data for {src} → {tgt}: {e}")

            # **Summary of Connections**
            print("\n📋 **Summary of Connections**")
            print("══════════════════════════════════════════════════")
            print(f"{'Source Area':<10} → {'Target Area':<10} | {'# Connections':<10}")
            print("══════════════════════════════════════════════════")

            heatmap_area = []
            for (src, tgt), count in connection_counts.items():
                print(f"{src:<10} → {tgt:<10} | {count:<10}")
                heatmap_area.append([src, tgt, count])
                
            heatmap_area = pd.DataFrame(heatmap_area, columns=["Area1","Area2", "NB_Connections"])
            heatmap_area = heatmap_area.pivot(index="Area1",columns="Area2",values="NB_Connections")
            
            print("══════════════════════════════════════════════════")
            print("✅ **All Connections Established Successfully!**\n")
            
            # Define the specific order of areas
            area_order = ['V1', 'TO', 'AT', 'PF_L', 'PM_L', 'M1_L', 'A1', 'AB', 'PB', 'PF_i', 'PM_i', 'M1_i']

            # Reorder rows and columns based on the specific order
            heatmap_area = heatmap_area.reindex(index=area_order, columns=area_order)

            # Plot heatmap
            plt.figure(figsize=(10, 8))
            sns.heatmap(heatmap_area, annot=True, fmt=".0f", cmap="viridis", linewidths=0.5)
            plt.title("Inter-Area Connection Heatmap")
            plt.xlabel("Target Area")
            plt.ylabel("Source Area")
            plt.xticks(rotation=45)
            plt.yticks(rotation=0)
            plt.savefig('./plot_training/heat_map_area.png')
            print("══════════════════════════════════════════════════")
            print("✅ **Heatmap Area saved in ./plot_training/heat_map_area.png!**\n")
            


        

    def connect_recorders(self):
        """
        Connect spike recorder.
        """

        self.spike_rec = nest.Create('felix_spike_recorder',
                                     {'record_to': 'ascii', 'label': 'felix'})
        self.vm = nest.Create('multimeter', params={'record_from': ["V_m", "I_tot",  "I_exc","I_inh", "I_noise"],
                                                    'record_to': 'ascii', 'label': 'V_m'})


        for area in self.areas.values():
            nest.Connect(area.exc, self.spike_rec)
            nest.Connect(self.vm, area.exc)



    # Now the `store` and `train_action_object` functions are part of FelixNet
    store = store  # Attaching store function to FelixNet class
    train_action_object = train_action_object  # Attaching train_action_object function to FelixNet class
    rebuild_net = rebuild_net
    reconnect_areas = reconnect_areas
    test_aud = test_aud
    test_art = test_art
    test_gui = test_gui
