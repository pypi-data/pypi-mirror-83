"""
This is the IR analysis sub-pakcage of RAP.

Author: Brian C. Ferrari
"""
from .config import *


from .get_peaks                 import get_peaks
from .make_heat_map             import make_heat_map
from .plot_all_spectra          import plot_all_spectra
from .plot_average_spectra      import plot_average_spectra
from .plot_nitrile_location     import plot_nitrile_location
from .plot_peak_counts          import plot_peak_counts
from .plot_peak_heights         import plot_peak_heights
from .plot_single_spectra       import plot_single_spectra
from .plot_zoomed_nitrile       import plot_zoomed_nitrile
from .save_peak_heights         import save_peak_heights
from .save_peak_locations       import save_peak_locations
from .subtract_spectra          import subtract_spectra
