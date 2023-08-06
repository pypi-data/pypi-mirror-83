import glob, os, sys
import numpy as np
import pandas as pd
import seaborn as sb
from collections import Counter
import matplotlib.pyplot as plt
from sklearn import preprocessing
from scipy.signal import find_peaks
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

#Class params()

def make_rectanlge(hi, low, color):
    w   = (4000-675)/5
    h   = (hi - low)/4
    X   = ((4000-675)/2) + 675 - w/2
    Y   = ((hi - low)/2) + low - h/2
    rec = Rectangle((X, Y), w, h, linewidth=1.75, linestyle='--',
                    edgecolor=color, facecolor='none')
    return rec


def catch_fail(col, im_str, folder):
    print(col)
    print(glob.glob(im_str))
    print(folder)
    return


def make_im_str(col, maindir, folder):
    star   = col.lower().replace(' ', '_').replace('(','').replace(')', '').replace('_no_as', '') + '_'
    im_str = maindir + folder + '/*' + star + '*.jpg'
    return im_str
