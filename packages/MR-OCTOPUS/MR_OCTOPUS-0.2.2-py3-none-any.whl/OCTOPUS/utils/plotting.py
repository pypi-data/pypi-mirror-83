# Copyright of the Board of Trustees of Columbia University in the City of New York
'''
Methods to plot the resulting images from off-resonance correction
\nAuthor: Marina Manso Jimeno
\nLast updated: 06/03/2020
'''
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1 import ImageGrid

def plot_correction_results(im_stack, col_names, row_names):
    '''
    Creates a plot with the resulting correction images in a grid

    Parameters
    ----------
    im_stack : numpy.ndarray
        Stack of images. [0] Corrupted images, [1]-[len(im_stack] corrected images using the different methods
    col_names : tuple
        Titles for the columns of the plot. Correction methods.
    row_names : tuple
        Titles for the rows of the plot. Off-resonance frequency ranges.
    '''
    if len(row_names) == 1:
        im_stack = np.expand_dims(im_stack, axis=-1)

    nrows = im_stack.shape[-1]
    ncols = im_stack.shape[0]

    im_list = []
    for frange in range(nrows):
        for method in range(ncols):
            im_list.append(np.abs(np.squeeze(im_stack[method, :, :, frange])))

    fig = plt.figure()
    grid = ImageGrid(fig, 111,  # similar to subplot(111)
                     nrows_ncols=(nrows, ncols),  # creates 2x2 grid of axes
                     axes_pad=0,  # pad between axes in inch.
                     )

    for ax, im, c in zip(grid, [im for im in im_list], [count for count in range(len(im_list))]):
        # Iterating over the grid returns the Axes.
        ax.imshow(im, cmap='gray')
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        if range(ncols).count(c):
            ax.set_title(col_names[c])
        if list(np.arange(nrows)*ncols).count(c):
            ax.yaxis.set_visible(True)
            ax.yaxis.set_ticks([])
            ax.yaxis.set_label_text(row_names[int(c/ncols)], fontsize=12)

    plt.show()

