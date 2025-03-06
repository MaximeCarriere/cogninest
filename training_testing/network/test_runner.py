import os
import sys
# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config_testing import NETWORKS, NETWORKS_DIR, TESTING_OUTPUT_DIR, NETWORKS_LIST, TEST_MODE
from utils.file_operations import ensure_directory_exists
from network import FelixNet  # Ensure FelixNet is imported
import pickle
import pandas as pd
import numpy as np  # Ensure numpy is available

def run_all_tests():
    """Run tests on all saved networks based on TEST_MODE in config.py."""
    print("🚀 Starting FelixNet Testing...")

    for network in NETWORKS:
        print(f"🧪 Testing Network: {network}")

        network_path = os.path.join(NETWORKS_DIR, network)
        output_path = os.path.join(TESTING_OUTPUT_DIR, f"testing_{network}")

        # Ensure output directory exists
        ensure_directory_exists(output_path)

        if TEST_MODE == "auditory":
            print(f"🎵 Running auditory tests for {network}")
            testing_auditory_multiple_networks(NETWORKS_LIST, network_path, output_path)

        elif TEST_MODE == "articulatory":
            print(f"🗣️ Running articulatory tests for {network}")
            testing_articulatory_multiple_networks(NETWORKS_LIST, network_path, output_path)

        elif TEST_MODE == "both":
            print(f"🎵🗣️ Running both auditory and articulatory tests for {network}")
            testing_auditory_multiple_networks(NETWORKS_LIST, network_path, output_path)
            testing_articulatory_multiple_networks(NETWORKS_LIST, network_path, output_path)

    print("✅ All tests completed!")

def safe_pickle_load(file_path):
    """ Load a pickle file safely, even if numpy is missing. """
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)  # Normal loading
    except ModuleNotFoundError as e:
        if "numpy" in str(e):  # Handle missing numpy
            print(f"⚠️ Warning: NumPy is missing when loading {file_path}, attempting fallback.")
            with open(file_path, "rb") as f:
                network = pickle.load(f, encoding="latin1")
            
            # Convert NumPy arrays to lists
            for key in network.keys():
                if isinstance(network[key], np.ndarray):
                    network[key] = network[key].tolist()
            return network
        else:
            raise e  # Raise other errors


def testing_auditory_multiple_networks(networks_list, networks_dir, network_out):
    """ Test auditory networks. """
    print("network_out: ", network_out)
    ensure_directory_exists(network_out)

    for patt_no_count in networks_list:
        print("##############################")
        print(f"     NETWORK: {patt_no_count}")
        print("##############################")

        filename = f"network_{patt_no_count}"
        directory_network = f"{networks_dir}/{filename}".strip()  # Remove accidental spaces
        print(directory_network)
        
        network = safe_pickle_load(directory_network)  # Load safely

        audi = network["pattern_auditory"]
        arti = network["pattern_articulatory"]

        f = FelixNet()
        f.rebuild_net(directory_network)

        # Check if test_aud exists in FelixNet before calling
        if hasattr(f, 'test_aud'):
            f.test_aud(audi, arti, patt_no_count, num_reps=10, t_on=2, t_off=30)
        else:
            print("⚠️ Warning: `test_aud` method is missing in FelixNet!")

    print("✅ Testing Auditory Completed")


def testing_articulatory_multiple_networks(networks_list, networks_dir, network_out):
    """ Test articulatory networks. """
    ensure_directory_exists(network_out)

    for patt_no_count in networks_list:
        print("##############################")
        print(f"     NETWORK: {patt_no_count}")
        print("##############################")

        filename = f"network_{patt_no_count}"
        directory_network = f"{networks_dir}/{filename}".strip()  # Remove accidental spaces

        network = safe_pickle_load(directory_network)  # Load safely

        audi = network["pattern_auditory"]
        arti = network["pattern_articulatory"]

        f = FelixNet()
        f.rebuild_net(directory_network)

        # Check if test_art exists in FelixNet before calling
        if hasattr(f, 'test_art'):
            f.test_art(audi, arti, patt_no_count, num_reps=10, t_on=2, t_off=30)
        else:
            print("⚠️ Warning: `test_art` method is missing in FelixNet!")


    print("✅ Testing Articulatory Completed")
