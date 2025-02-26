# bogy-music-vis

Artistic music visualization with PyGame


## Setup

- `py -m venv .venv`
- Windows: `.venv\Scripts\activate`, Other: `source .venv/bin/activate`
- `pip install -r .\requirements.txt`
- If pygame install has issues: `py -m pip install -U pygame`


## Start Game

- `py game.py`


## Add New Music

- Add .wav or .mp3 file in `audio/` folder
- `py preprocess.py`
- `py preprocess.py IRIS.wav` (replace IRIS.wav with you filename)


## PyGame

- https://coderslegacy.com/python/python-pygame-tutorial/
- https://www.pygame.org/docs/
- https://www.pygame.org/docs/ref/examples.html

## Color

- https://matplotlib.org/stable/gallery/color/colormap_reference.html
- https://matplotlib.org/stable/gallery/color/individual_colors_from_cmap.html
