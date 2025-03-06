import pickle
import time
from pathlib import Path
import matplotlib.pyplot as plt
import random
import numpy as np
import pandas as pd
from IPython.display import display
import seaborn as sns
import re
import os
from config import *
import shutil

def ensure_directory_exists(directory, clear=False):
    """
    Ensure that the given directory exists. If it doesn't, create it.
    If `clear=True`, remove all files inside before proceeding.

    Args:
    - directory (str): The directory path to ensure exists.
    - clear (bool): If True, delete all files inside the directory before proceeding.
    """
    if os.path.exists(directory):
        if clear:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Remove file or symbolic link
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Remove directory and its contents
                except Exception as e:
                    print(f"⚠️ Error deleting {file_path}: {e}")
        else:
            print(f"✅ Directory '{directory}' already exists. No files deleted.")
    else:
        os.makedirs(directory)
        print(f"📁 Created directory '{directory}'.")



def save_network(filename, network_data):
    ensure_directory_exists("./save_network/")
    with open(f"./save_network/{filename}", "wb") as f:
        pickle.dump(network_data, f, pickle.HIGHEST_PROTOCOL)

