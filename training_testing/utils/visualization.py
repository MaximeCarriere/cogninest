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
import gc
import shutil
from utils.file_operations import *

def plot_activation(data, pattern_no):
    plt.figure(figsize=(10, 5))
    plt.plot(data['sum'])
    plt.title(f"Activation Pattern {pattern_no}")
    plt.xlabel("Time")
    plt.ylabel("Activation")
    plt.show()


def show_owerlapp_pattern(motor, visu, audi, arti):

    print("#################")
    print("CHECKING OVERLAPP")
    print("#################")

    ensure_directory_exists("./plot_training")
    # Sample data (replace with your actual list of lists)
    s = {'Visual': visu, 'Motor': motor, 'Auditory': audi, 'Articulatory': arti}
    
    rows, cols = 2, 2  # Define number of rows and columns for subplots
    plot_number = 1  # Counter for subplot numbering within the grid
    
    for sys, data in s.items():
      # Calculate overlap for each pair of lists
      overlap_matrix = np.zeros((len(data), len(data)))
      for i in range(len(data)):
        for j in range(i, len(data)):  # Avoid calculating twice (i, j) and (j, i)
          overlap_matrix[i, j] = len(set(data[i]) & set(data[j]))  # Count intersection
    
      # Fill the other half of the matrix symmetrically
      overlap_matrix += overlap_matrix.T - np.diag(overlap_matrix.diagonal())
    
      # Subplot position based on plot_number
      plt.subplot(rows, cols, plot_number)
      ax = sns.heatmap(overlap_matrix, cmap='YlGnBu', annot=True)  # Annotate with values
    
      # Add labels and title (optional)
      plt.xlabel('Pattern')
      plt.ylabel('Pattern')
      plt.title(f'Overlap Heatmap - {sys}')  # Add system name to title
    
      plot_number += 1  # Increment counter for next subplot
    
    plt.tight_layout()  # Adjust spacing between subplots
    


    plt.savefig('./plot_training/pattern_overlapp_matrix.png')
    plt.close()
    

def plot_pattern_presence(patterns, exc_neurons, filename):
    """
    Generates a subplot visualization of neuron presence for each pattern.

    Args:
    - patterns (list of lists): List of neuron indices for each pattern.
    - exc_neurons (int): Number of excitatory neurons per row/column.
    - filename (str): Name for the output plot image.
    """

    num_patterns = len(patterns)
    cols = min(4, num_patterns)  # Limit to 4 columns
    rows = (num_patterns // cols) + (num_patterns % cols > 0)  # Calculate required rows

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))  # Dynamic figure size
    axes = np.array(axes).reshape(rows, cols)  # Ensure axes are in a 2D array for indexing

    for i, pattern in enumerate(patterns):
        row, col = divmod(i, cols)
        
        # Create presence matrix
        presence_matrix = np.zeros((exc_neurons, exc_neurons))
        for neuron in pattern:
            r, c = divmod(neuron, exc_neurons)
            presence_matrix[r, c] = 1  # Mark presence

        ax = axes[row, col]  # Select subplot
        sns.heatmap(presence_matrix, cmap="Blues", linewidths=0.1, linecolor="black", square=True, ax=ax)
        ax.set_title(f"Pattern {i+1}")  # Title for each pattern
        ax.set_xticks([])  # Remove axis labels for clarity
        ax.set_yticks([])

    # Hide empty subplots
    for i in range(num_patterns, rows * cols):
        fig.delaxes(axes.flatten()[i])

    # Save the figure
    output_dir = "./plot_training"
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, f"{filename}.png")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    print(f"✅ Pattern presence subplot saved: {save_path}")


def save_plot_activation_new(pres, dat, patt_no):
    plt.rcParams["figure.figsize"] = (20, 10)
    
    to_plot = dat.pivot(index="time", columns="AreaAbs", values="sum").fillna(0).stack().reset_index()
    time_tot = pd.DataFrame([k for k in range(int(to_plot.time.min()), int(to_plot.time.max()))], columns=["time"])

    #print(str(patt_no) + "   "+str(pres))
    fig, ax = plt.subplots()
    for j in range(12):
        plt.subplot(2, 6, j + 1)
        area_dat = to_plot[to_plot.AreaAbs == j]
        eph = pd.concat([area_dat.set_index("time"), time_tot.set_index("time")], axis=1)
        eph["AreaAbs"] = j
        eph[0] = eph[0].fillna(0)
        sns.lineplot(data=eph, x="time", y=0, linewidth=5)
        plt.title("Area: " + str(j) + "  Max: "+str(eph[0].max()))
        #print("Area: " + str(j) + "  Max: "+str(eph[0].max()))
        plt.xlim([to_plot.time.min(), to_plot.time.max()])
        plt.axhline(y=0, color='red', linestyle='--')
        plt.axhline(y=19, color='green', linestyle='--')
        plt.ylim([0, 80])
        plt.xlim([to_plot["time"].min(), to_plot["time"].min() + 30])
    
    plt.suptitle("Patt_no: " + str(patt_no) + '   NB Pres: ' + str(pres))
    plt.savefig('./plot_training/plot_activation_0.png')
    
    plt.clf()  # Clear the current figure
    plt.cla()  # Clear the current axes
    plt.close('all')  # Close all figures

    gc.collect()  # Run garbage collection
