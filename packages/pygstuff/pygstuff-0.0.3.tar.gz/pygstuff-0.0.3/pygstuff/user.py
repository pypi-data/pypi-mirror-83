#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''user stuff
user.pressed_somekey()
user.held_somekey
user.quit
'''

import pygame

def pressed_x(event, key_pressed, key_mods):
    '''Return True when x is pressed.'''
    return (
        event.type == pygame.KEYDOWN
        and
        key_pressed[pygame.K_x]
        and not
        held_Shift(key_mods)
        )

def pressed_X(event, key_pressed, key_mods):
    '''Return True when Shift+x is pressed.'''
    return (
        event.type == pygame.KEYDOWN
        and
        key_pressed[pygame.K_x]
        and
        held_Shift(key_mods)
        )

def pressed_spacebar(event, key_pressed):
    '''Return True when spacebar is pressed.'''
    return (
        event.type == pygame.KEYDOWN
        and
        key_pressed[pygame.K_SPACE]
        )

def pressed_a(event, key_pressed, key_mods):
    '''Return True when "a" is pressed.'''
    return (
        event.type == pygame.KEYDOWN
        and
        key_pressed[pygame.K_a]
        and not
        held_Shift(key_mods)
        )

def pressed_right(event, key_pressed, key_mods):
    '''Return True when l is pressed.'''
    return (
        event.type == pygame.KEYDOWN
        and
        key_pressed[pygame.K_l]
        and not
        held_Shift(key_mods)
        )

def pressed_up(event, key_pressed, key_mods):
    '''Return True when k is pressed.'''
    return (
        event.type == pygame.KEYDOWN
        and
        key_pressed[pygame.K_k]
        and not
        held_Shift(key_mods)
        )

def pressed_left(event, key_pressed, key_mods):
    '''Return True when h is pressed.'''
    return (
        event.type == pygame.KEYDOWN
        and
        key_pressed[pygame.K_h]
        and not
        held_Shift(key_mods)
        )

def pressed_down(event, key_pressed, key_mods):
    '''Return True when j is pressed.'''
    return (
        event.type == pygame.KEYDOWN
        and
        key_pressed[pygame.K_j]
        and not
        held_Shift(key_mods)
        )

def pressed_home(event, key_pressed, key_mods):
    '''Return True when 0 is pressed.'''
    return (
        event.type == pygame.KEYDOWN
        and
        key_pressed[pygame.K_0]
        and not
        held_Shift(key_mods)
        )

def pressed_end(event, key_pressed, key_mods):
    '''Return True when $ (Shift+4) is pressed.'''
    return (
        event.type == pygame.KEYDOWN
        and
        key_pressed[pygame.K_4]
        and
        held_Shift(key_mods)
        )

def held_Shift(key_mods):
    '''Return True as long as Shift is held down.'''
    return key_mods & pygame.KMOD_SHIFT

def held_Ctrl(key_mods):
    '''Return True as long as Ctrl is held down.'''
    return key_mods & pygame.KMOD_CTRL

def quit(event, key_pressed, key_mods):
    '''Returns True if user clicks window-close or shortcut-key quits.

    Parameters
    ----------
    'event'
        A message from the message list returned by
        'pygame.event.get()'.
        Quit if 'event.type' is 'pygame.QUIT'.
    'key_pressed'
        Boolean array returned by 'pygame.key.get_pressed()'.
        Use key constant values to index the array.
        Example: key_pressed[pygame.K_q]
    'key_mods'
        Bitmask of all modifier keys held down.
        Returned by 'pygame.key.get_mods()'.
        Use bitwise operators to test if keys are held.
        Example: key_mods & pygame.KMOD_CTRL

    Examples
    --------
    pygame.init()
    display = pygame.display.set_mode( (100,100) )
    quit = False
    while not quit:
        for event in pygame.event.get():
            quit = quit(
                event,
                pygame.key.get_pressed(),
                pygame.key.get_mods()
                )
    '''
    def clicked_red_x(event): return event.type == pygame.QUIT
    def pressed_q(event, key_pressed):
        return (
            event.type == pygame.KEYDOWN
            and
            key_pressed[pygame.K_q]
            )
    return(clicked_red_x(event)
       or (held_Ctrl(key_mods)
          and pressed_q(event, key_pressed))
       or (pressed_q(event, key_pressed))
       )
