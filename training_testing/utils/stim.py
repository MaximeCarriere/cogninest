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


def stim_specs_patt_no(f, patt_no, nb_pattern, motor, visu, audi, arti, stim_strength):


    if (patt_no + 1 <= (nb_pattern/2)):
        
        stim_specs={'V1': {'neurons': visu[patt_no],
                                'I_stim': stim_strength},
                         'M1_L': {'neurons': f.neurons2IDs(random.sample(list(range(0,625)),19)),
                                'I_stim':  stim_strength},
                         'A1': {'neurons': audi[patt_no],
                                'I_stim':  stim_strength},
                         'M1_i': {'neurons': arti[patt_no],
                               'I_stim':  stim_strength}}
 

    else:

        stim_specs ={'V1': {'neurons': f.neurons2IDs(random.sample(list(range(0,625)),19)),
                            'I_stim':  stim_strength},
                     'M1_L': {'neurons': motor[patt_no],
                            'I_stim':  stim_strength},
                     'A1': {'neurons': audi[patt_no],
                            'I_stim':  stim_strength},
                     'M1_i': {'neurons': arti[patt_no],
                            'I_stim':  stim_strength}}
       

    return stim_specs


def stim_specs_patt_no_gui(auditory_input,
                articulatory_input,
                visual_input,
                motor_input,
                patt_no,
                num_reps,
                t_on,
                t_off,
                auditory_check,
                articulatory_check,
                visual_check,
                motor_check,
                stim_strength):
                
    
    stim_specs={}
    if auditory_check==True:
            stim_specs['A1'] =  {'neurons': auditory_input[patt_no],
                            'I_stim':   stim_strength}
                            
    if articulatory_check==True:
            stim_specs['M1_i'] =  {'neurons': articulatory_input[patt_no],
                            'I_stim':   stim_strength}
    
    if motor_check==True:
            stim_specs['M1_L'] =  {'neurons': motor_input[patt_no],
                            'I_stim':   stim_strength}
                            
    if visual_check==True:
            stim_specs['V1'] =  {'neurons': visual_input[patt_no],
                            'I_stim':   stim_strength}
                            
                            
    return stim_specs


def stim_specs_patt_no_testing_audi_only(audi, patt_no, stim_strength):

    stim_specs={'A1': {'neurons': audi[patt_no],
                            'I_stim':   stim_strength}}

    return stim_specs
    
    
def stim_specs_patt_no_testing_arti_only(arti, patt_no, stim_strength):

    stim_specs={'M1_i': {'neurons': arti[patt_no],
                            'I_stim':   stim_strength}}

    return stim_specs
