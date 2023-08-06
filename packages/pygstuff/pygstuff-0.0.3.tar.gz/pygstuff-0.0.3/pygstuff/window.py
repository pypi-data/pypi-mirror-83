#!python.exe
# -*- coding: utf-8 -*-

import pygame
import os

class Window(object):
    '''The game window.

    Usage
    -----
    Create one Window instance at the start of the game script.

    See methods __init__ and open_window.

    Example
    -------
    >>> import pygame
    >>> import pygstuff as pygs
    >>> win=pygs.Window()
    >>> win.open_window(400,100)
    >>> import time
    >>> time.sleep(0.5) # window visible for 0.5 seconds
    '''
    def __init__(self, caption='Me game', icon=None):
        '''Window configuration.

        - calls pygame.init()
        - sets OS environment variable to center the window
        - sets the window caption (default is 'Me game')
        - sets the window icon (default is the Pygame logo)
        
        TODO
        ----
        add full-screen
        '''
        os.environ['SDL_VIDEO_CENTERED'] = '1' # do before pygame.init()
        pygame.init()
        pygame.display.set_caption(caption) # window title
        if icon is not None:
            pygame.display.set_icon(pygame.image.load(icon))

    def open_window(self, width=1200, height=600):
        '''Open the game window.

        - makes the game window appear
        - calls pygame.display.set_mode()
        - attribute 'surface' is the pygame Surface returned by
          pygame.display.set_mode
        - parameters 'width' and 'height' become attributes
          'width' and 'height'

        Parameters
        ----------
        width: pixel columns
        height: pixel rows
        '''
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode(
            # size=(self.width, self.height),
            (self.width, self.height),
            # flags=0,
            # depth=0,
            # display=0,
            ) # -> Surface

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
