#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Draw 2D geometry types.

This takes the 2D geometry types defined in pygstuff.geometry and
makes pygame calls to draw those geometries. There are two
reasons I wrote this module:

- hide manipulation of pixel coordinates from the application
  developer
- decouple drawing to the screen from doing 2D geometry

This goes beyond just dealing with y=0 referring to the top of
the screen. Here are the ideas:

integer pixel values
    The draw functions in this module round floating point
    coordinates to the nearest integer when drawing the 2D
    geometry type.
origin
    Control 2D geometry origin by specifiying it relative to the
    center of the pygame window. The default origin (0,0)
    places the 2D geometry origin at the center of the pygame
    window. Changing the origin behaves with backwards y.
    For example, origin (100,200) is 100 pixels right and 200
    pixels down from the center of the pygame window.
scale
     Control the pygame window view scale. It is usually
     inconvenient to be stuck with one drawing unit equal to one
     pixel.
"""
import pygame
import pygstuff as pygs

# ------------------------
# | Map points to pixels |
# ------------------------

# (Lazy me is using globals)
# pcsys is the PixelCoordinateSystem
# pcsys = {'scale':32, 'origin':pygs.Point(100,100)}
pcsys = {'scale':1, 'origin':pygs.Point(0,0)}

def pix_coord(
    point:pygs.Point,
    window:pygs.Window,
    pcsys:dict = pcsys
    ) -> pygs.Point:
    """Return pixel coordinates for a point.

    Use the pixel coordinate system's origin and scale to interpret the
    coordinates of the geometric point as a pixel in the window.

    Parameters
    ----------
    point
        (x,y) point following the standard conventions:

        - positive x is to the right
        - positive y is upward

    window
        A pygame window, as defined by pygs.

    pcsys
        Pixel coordinate system. I set this up as a global dict in the
        application, maybe I'll think of something better later.

        scale
            Coordinate system scale.
            At scale N, one pixel is N drawing units.

            For example, if scale=2 then one pixel is two drawing units.

        origin
            Coordinate system origin defined relative to the center of
            the window.

            For example, if ``origin`` is the point (0,0), the
            coordinate system origin is the center of the window.

    Return
    ------
    pygs.Point
        Pixel coordinates of the point for the given window.

    Example
    -------
    Specify the window dimensions
    >>> width = 1200; height = 600

    Make a game window
    >>> import pygstuff as pygs
    >>> win = pygs.Window()
    >>> win.open_window(width, height)

    Create a pixel coordinate system
    >>> pix_coord_sys = {'scale':1, 'origin':pygs.Point(0,0)}

    Create a point in the center of the screen
    >>> my_point = pygs.Point(0,0)
    >>> print(pix_coord(my_point, win, pix_coord_sys))
    Point(x=600, y=300)

    Create a point a bit to the right and up from the center
    >>> my_point = pygs.Point(50,100)
    >>> print(pix_coord(my_point, win, pix_coord_sys))
    Point(x=650, y=200)

    Create a point at a fractional pixel
    >>> my_point = pygs.Point(0.51,0.5)
    >>> print(pix_coord(my_point, win, pix_coord_sys))
    Point(x=601, y=300)
    """

    # The pcsys origin is defined relative to the window center.
    window_center = pygs.Point(round(window.width/2), round(window.height/2))

    # Map geometry origin to pixel origin.
    origin = pygs.PointMath.add([window_center, pcsys['origin']])

    # Calculate pixel x,y:
    # - shift relative to origin
    # - scale
    # - pixels must be integers, so round to nearest integer
    x = origin.x + round(point.x/pcsys['scale'])
    y = origin.y - round(point.y/pcsys['scale'])

    # TODO: decide if I care whether the pixel is visible...
    # like how much computational effort is wasted drawing as if the
    # screen is infinitely big...

    return pygs.Point(x,y)

def pix_coords(
        points:list,
        window:pygs.Window,
        pcsys:dict = pcsys
        ) -> list:
    """Return a list of pixel coordinates for a list of points.

    Use the center of the window as the origin to interpret the
    coordinates of the points.

    Parameters
    ----------
    points
        [(x1,y1), (x2,y2), ..., (xN,yN)] is a list of points
        following the standard conventions:

        - positive x is to the right
        - positive y is upward

        When using :func:`pix_coords` to draw lines, the points
        are connected with straight lines in the order they are
        listed.

    window, pcsys
        See :func:`pix_coord`.

    Return
    ------
    list
        List of the pixel coordinates of the points for the given
        window.

    Example
    -------
    Specify the window dimensions
    >>> width = 1200; height = 600

    Make a game window
    >>> import pygstuff as pygs
    >>> win = pygs.Window()
    >>> win.open_window(width, height)

    Make three points
    >>> a = pygs.Point(-5,0)
    >>> b = pygs.Point(5,0)
    >>> c = pygs.Point(5,10)

    Create a pixel coordinate system (origin 0,0 is the window center)
    >>> pix_coord_sys = {'scale':1, 'origin':pygs.Point(0,0)}

    Get the pixel coordinates for these points in the window
    >>> pix_coords([a,b,c], win, pix_coord_sys)
    [Point(x=595, y=300), Point(x=605, y=300), Point(x=605, y=290)]

    Get the pixel coordinates for the endpoints of a line segment
    >>> l = pygs.LineSegment.from_length(2)
    >>> pix_coords(l.endpoints, win, pix_coord_sys)
    [Point(x=599, y=300), Point(x=601, y=300)]
    """
    return [pix_coord(point, window, pcsys) for point in points]

def draw_lineseg(
        l:pygs.LineSegment,
        window:pygs.Window,
        pcsys:dict = pcsys, # PixelCoordinateSystem
        rgb:tuple=(255,255,255)
        ) -> None:
    """Draw a line segment in the window.

    """
    pygame.draw.aalines(
        window.surface,
        rgb,
        False, # if True, connect first and last points
        pix_coords(l.endpoints, window, pcsys)
        )

def draw_connect_points(
        points:list,
        window:pygs.Window,
        pcsys:dict = pcsys, # PixelCoordinateSystem
        rgb:tuple=(255,255,255)
        ) -> None:
    """Draw line segments connecting the list of points.

    """
    pygame.draw.aalines(
        window.surface,
        rgb,
        False, # if True, connect first and last points
        pix_coords(points, window, pcsys)
        )

