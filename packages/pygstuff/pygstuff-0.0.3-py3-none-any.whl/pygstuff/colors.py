'''Colors

Credit color scheme to Steve Losh, author of badwolf.vim

Example
-------
>>> import pygame
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
>>> import pygstuff as pygs
>>> hex_color = pygs.HEX()
>>> hex_color.tardis
'#0a9dff'

Example
-------
>>> import pygame
>>> import pygstuff as pygs
>>> rgb_color = pygs.RGB()
>>> rgb_color.tardis
(10, 157, 255)
'''

from collections import namedtuple

# All color names, values, and descriptions are credited to Steve Losh.
_badwolf_names = [
    # 'name'            (R,G,B)           ['HEX', 256-color-term]
    # Normal text.
    'plain'         , # (248,246,242)   = ['f8f6f2', 15]
    # Pure and simple.
    'snow'          , # (255,255,255)   = ['ffffff', 15]
    'coal'          , # (0,0,0)         = ['000000', 16]
    # Gravel colors based on a brown from Clouds Midnight.
    'brightgravel'  , # (217,206,195)   = ['d9cec3', 252]
    'lightgravel'   , # (153,143,132)   = ['998f84', 245]
    'gravel'        , # (133,127,120)   = ['857f78', 243]
    'mediumgravel'  , # (102,100,98)    = ['666462', 241]
    'deepgravel'    , # (69,65,59)      = ['45413b', 238]
    'deepergravel'  , # (53,50,45)      = ['35322d', 236]
    'darkgravel'    , # (36,35,33)      = ['242321', 235]
    'blackgravel'   , # (28,27,26)      = ['1c1b1a', 233]
    'blackestgravel', # (20,20,19)      = ['141413', 232]
    # From highlight in photo of a glass of Dale's Pale Ale on my desk.
    'dalespale'     , # (250,222,62)    = ['fade3e', 221]
    # A beautiful tan from Tomorrow Night.
    'dirtyblonde'   , # (244,207,134)   = ['f4cf86', 222]
    # Delicious, chewy red from Made of Code for poppiest highlights.
    'taffy'         , # (255,44,75)     = ['ff2c4b', 196]
    # Another chewy accent, but use sparingly!
    'saltwatertaffy', # (140,255,186)   = ['8cffba', 121]
    # Use for things that denote 'where the user is'
    'tardis',         # (10,157,255)    = ['0a9dff', 39]
    # This one's from Mustang, not Florida!
    'orange',         # (255,167,36)    = ['ffa724', 214]
    # A limier green from Getafe.
    'lime',           # (174,238,0)     = ['aeee00', 154]
    # Rose's dress in The Idiot's Lantern.
    'dress',          # (255,158,184)   = ['ff9eb8', 211]
    # Another play on the brown from Clouds Midnight.
    'toffee',         # (184,136,83)    = ['b88853', 137]
    # Also based on that Clouds Midnight brown.
    'coffee',         # (199,145,91)    = ['c7915b', 173]
    'darkroast'       # (136,99,63)     = ['88633f', 95]
    ]

_badwolf_hex = (
    # Normal text.
    '#f8f6f2',
    # Pure and simple.
    '#ffffff',
    '#000000',
    # Gravel colors based on a brown from Clouds Midnight.
    '#d9cec3',
    '#998f84',
    '#857f78',
    '#666462',
    '#45413b',
    '#35322d',
    '#242321',
    '#1c1b1a',
    '#141413',
    # From highlight in photo of a glass of Dale's Pale Ale on my desk.
    '#fade3e',
    # A beautiful tan from Tomorrow Night.
    '#f4cf86',
    # Delicious, chewy red from Made of Code for poppiest highlights.
    '#ff2c4b',
    # Another chewy accent, but use sparingly!
    '#8cffba',
    # Use for things that denote 'where the user is'
    '#0a9dff',
    # This one's from Mustang, not Florida!
    '#ffa724',
    # A limier green from Getafe.
    '#aeee00',
    # Rose's dress in The Idiot's Lantern.
    '#ff9eb8',
    # Another play on the brown from Clouds Midnight.
    '#b88853',
    # Also based on that Clouds Midnight brown.
    '#c7915b',
    '#88633f',
    )

_badwolf_rgb = (
    # Normal text.
    (248,246,242),
    # Pure and simple.
    (255,255,255),
    (0,0,0),
    # Gravel colors based on a brown from Clouds Midnight.
    (217,206,195),
    (153,143,132),
    (133,127,120),
    (102,100,98),
    (69,65,59),
    (53,50,45),
    (36,35,33),
    (28,27,26),
    (20,20,19),
    # From highlight in photo of a glass of Dale's Pale Ale on my desk.
    (250,222,62),
    # A beautiful tan from Tomorrow Night.
    (244,207,134),
    # Delicious, chewy red from Made of Code for poppiest highlights.
    (255,44,75),
    # Another chewy accent, but use sparingly!
    (140,255,186),
    # Use for things that denote 'where the user is'
    (10,157,255),
    # This one's from Mustang, not Florida!
    (255,167,36),
    # A limier green from Getafe.
    (174,238,0),
    # Rose's dress in The Idiot's Lantern.
    (255,158,184),
    # Another play on the brown from Clouds Midnight.
    (184,136,83),
    # Also based on that Clouds Midnight brown.
    (199,145,91),
    (136,99,63)
    )

# namedtuple "defaults" keyword requires Python >= 3.7
RGB = namedtuple(
    'RGB', # typename
    _badwolf_names, # list of color names from badwolf
    defaults=_badwolf_rgb # list of color values in RGB format
    )

HEX = namedtuple(
    'HEX', # typename
    _badwolf_names, # list of color names from badwolf
    defaults=_badwolf_hex # list of color values in hex format
    )

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
