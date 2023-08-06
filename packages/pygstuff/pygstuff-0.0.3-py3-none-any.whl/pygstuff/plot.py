#!python.exe
# -*- coding: utf-8 -*-
'''plot stuff
get_data(filepath, col) -> list
scale_data_to_fit(data, size) -> list

TODO
----
[ ] finish moving plotting stuff from $games/plot-1d.py
'''

import pygame

def _strings_from_data_columns(filepath) -> list:
    '''Read data file found at `filepath`.
    Ignore comment lines.
    Return each data column as a tuple of strings.
    The tuples are returned as a list:
        list index 0 is column 0,
        list index 1 is column 1,
        etc.
    The length of the returned list is the number of columns in the data file.

    Parameters
    ----------
    filepath: path to data file

    Data file format
    ----------------
    - comments (ignored) begin with '#'
    - columns are tab-separated
    - file contains one or more columns

    Example
    -------
    Get a path to the data file.
    >>> from pathlib import Path
    >>> filepath = Path('plot-example-data/_xy_data.txt')

    Read the data as strings.
    >>> import pygstuff as pygs
    >>> data = pygs.plot._strings_from_data_columns(filepath)

    It is data for an XY plot. Expect two columns.
    >>> len(data)
    2
    '''
    with open(filepath) as datafile:
        data = (
            line.strip('\n').split('\t') # '1\t2\n' -> ['1', '2']
            for line in datafile
            if not line.startswith('#') # ignore header lines
            )
        # Unzip the data into a tuple for each column.
        return tuple(zip(*iter(data)))

def get_data(filepath, col=0) -> list:
    '''Return data in column number `col` as a list of floating point values.

    Parameters
    ----------
    filepath: (pathlib.Path) path to data file
    col: (int) the column number

    Example
    -------
    Get a path to the data file.
    >>> from pathlib import Path
    >>> filepath = Path('plot-example-data/_xy_data.txt')

    Get data in column 0 and column 1 as floats.
    >>> x = get_data(filepath, col=0)
    >>> y = get_data(filepath, col=1)

    The data is a list.
    >>> type(x)
    <class 'list'>
    >>> type(y)
    <class 'list'>

    The two columns are the same length.
    >>> len(x)
    957
    >>> len(y)
    957

    The greatest x value is usually the last x value.
    >>> x[-1] == max(x)
    True

    The greatest y value is usually not the last y value.
    >>> y[-1] != max(y)
    True

    The entries in the x and y lists are type float.
    >>> type(x[0])
    <class 'float'>
    >>> type(max(y))
    <class 'float'>
    '''
    data = _strings_from_data_columns(filepath)
    floats = (float(x) for x in data[col])
    return list(iter(floats))

def scale_data_to_fit(data, size) -> list:
    '''Autoscale data to dimension "size" in pixels.

    TODO
    ----
    Give this some more thought.
    Does the scaling make sense for x-values too?
    What I'm really after is the pixel values to use.
    So the scaling effect is like a zoom, right?
    It should replace the actual values with the pixel-x or
    pixel-y that achieves the desired placement.

    Rename this "zoom" and add parameter index_range, defaulting
    to the full data set (index_range 0 to len(data)).

    Leave it up to the caller to flip the data.

    Leave it up to the caller to offset the data within the
    desired window area.

    Parameters
    ----------
    data: list of floats returned by get_data()
    size: size to fit within, in units of pixels

    Example
    -------
    Get the y values to plot.
    >>> from pathlib import Path
    >>> filepath = Path('plot-example-data/_xy_data.txt')
    >>> y = get_data(filepath, col=1)

    Make the plot 500 pixels tall.
    >>> plot_height = 500
    >>> scaled_data = scale_data_to_fit(y, plot_height)
    >>> type(scaled_data)
    <class 'list'>
    '''
    scale = size/( max(data) - min(data) )
    return [ val*scale for val in data ]

def scale_data_to_fixed_yrange(data, size, yrange):
    '''Scale data to dimension "size" in pixels.'''
    scale = size/yrange
    return [ val*scale for val in data ]

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
