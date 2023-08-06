#!python.exe
# -*- coding: utf-8 -*-

import pygame

class Clock(object):
    '''The game clock.

    Usage: setup
    -----
    Create one Clock instance at the start of the game script.

    See method __init__().

    Example: setup
    -------
    >>> import pygstuff as pygs # assume pygame already imported
    >>> clock = pygs.Clock(framerate=50)

    Usage: loop
    -----
    Tick the clock on each iteration of the game loop.

    See method tick().

    Example: loop
    -------
    >>> clock.tick()
    '''
    def __init__(self, framerate=50):
        '''Clock configuration.

        - stores framerate as private attribute _framerate
        - calls pygame.time.Clock() and stores as private attribute _clock
        
        See method tick().
        
        Parameter
        ---------
        framerate:
            - rate at which game screen updates
                - bigger number means faster update
                - default is 50
            - update is throttled at the framerate:
                - game may run slower than framerate
                - but game cannot run faster than framerate
        '''
        self._framerate = framerate
        self._clock = pygame.time.Clock()
    def tick(self):
        '''Tick the game clock at rate _framerate.
        '''
        self._clock.tick(self._framerate)
if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

