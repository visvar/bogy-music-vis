# bogy-music-vis

Artistic music visualization with PyGame for python 3.13

Slides:
https://docs.google.com/presentation/d/1WAw0krJXZjp1Y4xFvjMmem2Q7ye7HvdrlRjKREvM8Vg/edit?usp=sharing


## Setup

- `python -m venv .venv`
- Windows: `.venv\Scripts\activate`, Other: `source .venv/bin/activate`
- `pip install -r .\requirements.txt`
- If pygame install has issues: `py -m pip install -U pygame`


## Start Game

- `python game.py`


## Add New Music

- Add .wav or .mp3 file in `audio/` folder
- `python preprocess.py`
- `python preprocess.py IRIS.wav` (replace IRIS.wav with you filename)


## Pre-build functions
gameBausteine.py includes some nice visualizations as functions and can be used for the beginning.

## PyGame

- https://coderslegacy.com/python/python-pygame-tutorial/
- https://www.pygame.org/docs/
- https://www.pygame.org/docs/ref/examples.html

## Color

- https://matplotlib.org/stable/gallery/color/colormap_reference.html
- https://matplotlib.org/stable/gallery/color/individual_colors_from_cmap.html
