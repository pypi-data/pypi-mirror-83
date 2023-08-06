""" This module uses a list of colours, called <colors>, the length of which = the of the number of cities that need to be highlighted in different colours.
    With a for loop it then creates a dictionary and attributes to each city [key] a color [value]
    
"""
import numpy as np
import matplotlib.pyplot as plt


def get_discrete_cmap(N, base_cmap=None):
    """Create an N-bin discrete colormap based on the specified input map. """
    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    
    return base.from_list(cmap_name, color_list, N)


def color_to_origin(df_nodes):
    """Assigns colors to origins."""
    raise NotImplementedError