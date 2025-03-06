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
from config.config_training import *



# Plotting helpers

def extract_events(data, time=None, sel=None):
    """Extract all events within a given time interval.

    Both time and sel may be used at the same time such that all
    events are extracted for which both conditions are true.

    Parameters
    ----------
    data : list
        Matrix such that
        data[:,0] is a vector of all gids and
        data[:,1] a vector with the corresponding time stamps.
    time : list, optional
        List with at most two entries such that
        time=[t_max] extracts all events with t< t_max
        time=[t_min, t_max] extracts all events with t_min <= t < t_max
    sel : list, optional
        List of gids such that
        sel=[gid1, ... , gidn] extracts all events from these gids.
        All others are discarded.

    Returns
    -------
    numpy.array
        List of events as (gid, t) tuples
    """
    val = []

    if time:
        t_max = time[-1]
        if len(time) > 1:
            t_min = time[0]
        else:
            t_min = 0

    for v in data:
        t = v[1]
        gid = v[0]
        if time and (t < t_min or t >= t_max):
            continue
        if not sel or gid in sel:
            val.append(v)

    return np.array(val)

def from_data(data, sel=None, **kwargs):
    """Plot raster plot from data array.

    Parameters
    ----------
    data : list
        Matrix such that
        data[:,0] is a vector of all gids and
        data[:,1] a vector with the corresponding time stamps.
    sel : list, optional
        List of gids such that
        sel=[gid1, ... , gidn] extracts all events from these gids.
        All others are discarded.
    kwargs:
        Parameters passed to _make_plot
    """
    ts = data[:, 1]
    d = extract_events(data, sel=sel)
    ts1 = d[:, 1]
    gids = d[:, 0]
    return d
    #return [ts, ts1, gids, data[:, 0]]

def from_file(fname, **kwargs):
    """Plot raster from file.

    Parameters
    ----------
    fname : str or tuple(str) or list(str)
        File name or list of file names

        If a list of files is given, the data from them is concatenated as if
        it had been stored in a single file - useful when MPI is enabled and
        data is logged separately for each MPI rank, for example.
    kwargs:
        Parameters passed to _make_plot
    """
    if isinstance(fname, str):
        fname = [fname]

    if isinstance(fname, (list, tuple)):
        try:
            global pandas
            pandas = __import__('pandas')
            return from_file_pandas(fname, **kwargs)
        except ImportError:
            from_file_numpy(fname, **kwargs)
    else:
        print('fname should be one of str/list(str)/tuple(str).')

def from_file_pandas(fname, **kwargs):
    """Use pandas."""
    data = None
    for f in fname:
        dataFrame = pandas.read_csv(
            f, sep='\s+', lineterminator='\n',
            header=None, index_col=None,
            skipinitialspace=True)
        newdata = dataFrame.values

        if data is None:
            data = newdata
        else:
            data = np.concatenate((data, newdata))
    return from_data(data, **kwargs)

    
def sender2area(sender):
    """Converts Felix sender ID to its corresponding area and ID in area"""

    remove_pg = {0:1,
             5: 2,
            6:3,
             11:4}


    #return [neuron+(1251*area_num) for neuron in neurons]
    for i in range(0,12):
        if i in [0, 5, 6, 11]:
            add = remove_pg[i]
        else:
            add = 0

        to_remove = EXC_NEURONS*EXC_NEURONS*2+1
        ID=sender-(to_remove*i)-add
        if ID <= EXC_NEURONS*EXC_NEURONS:
            area_num=i
            return ID, area_num
        else:
            continue
    #ID=sender-(1251*area_num)
    return sender, 99999999

def convert_nstr_to_pattern(nstr):
    '''If we don't cover this in class, use this function as follows:
        First, load matplotlib with 'import matplotlib.pyplot as plt'.
        example = '137;66;34' # write your neuron string here
        pattern = convert_nstr_to_pattern(example)
        plt.imshow(pattern)'''
    # convert nstr to nID as integers
    ns=[n-1 for n in nstr]

    area = np.zeros((EXC_NEURONS,EXC_NEURONS))

    # write 1 for each nID at the appropriate
    # position in the matrix
    for neuron in ns:
        row = int(neuron/EXC_NEURONS)
        col = neuron%EXC_NEURONS
        area[row][col] += 1

    #area[area>1]=1
    return area

def dat_from_file(string_pattern):
    """string_pattern - regex name pattern for data files to stitch together,
    i.e. 'felix-*.dat'"""
    dat = from_file([str(p) for p in Path('.').glob(string_pattern)])
    dat=pd.DataFrame(dat, columns=['sender','time','drop1','drop2'])
    dat=dat.drop(['drop1','drop2'], axis=1)
    dat=dat[pd.to_numeric(dat['sender'], errors='coerce').notnull()]
    dat=dat.reset_index(drop=True)
    dat.sender=dat.sender.astype(int)
    dat.time=dat.time.astype(float)
    dat.time=dat.time.apply(lambda x: np.round(x))
    dat.time=dat.time.astype(int)
    dat['ID']=dat.sender.apply(lambda x: sender2area(x)[0])
    dat['AreaAbs']=dat.sender.apply(lambda x: sender2area(x)[1])
    dat = dat.drop_duplicates()
    dat=dat.groupby(['AreaAbs','time'])['ID'].apply(list).reset_index(name='nstr')
    dat['matrix']=dat.nstr.apply(lambda x: convert_nstr_to_pattern(x))
    return dat


    ## Max function
def sum_arrays(row):
    return np.sum(row)
