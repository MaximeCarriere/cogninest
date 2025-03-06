# config.py

############################################################
                        # TESTING DATA
############################################################

TEST_MODE = "auditory"  # Options: "auditory", "articulatory", "both"

# Define parameters for testing
NUM_REPS = 4       # Number of repetitions/stimulations for testing
T_ON = 2           # Time stimulus is ON
T_OFF = 30          # Time stimulus is OFF
STIM_STRENGTH = 500 # Strength of stimulation / Other parameters will be similar
TESTING_OUTPUT_DIR = "./testing_data/"

# List of trained networks to be tested
NETWORKS = [
    "save_network"
]

# Directory where networks are stored
NETWORKS_DIR = "/Users/maximecarriere/src/nest_test/training_action_object_refracto/main/"

# ✅ Define the list of training steps for each network
NETWORKS_LIST = []

############################################################
                        # PLOTING DATA
############################################################

# Directory where networks are read/stored
TESTING_INPUT_GRAPH = "./testing_data/"
TESTING_OUTPUT_GRAPH = "./graph/"
NETWORKS_LIST_GRAPH = [10]
GRAPH_MODE = ["auditory"]#, "articulatory", "ca_size", "ca_size_over_threshold"]
#GRAPH_MODE = ["ca_size", "ca_size_over_threshold"]

