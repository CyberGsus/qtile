from os import listdir
from os import path
from collections import namedtuple
import json


dimensions = namedtuple('dimensions', ('width', 'height'), defaults = (0, 0))



bar_dimensions = dimensions(24)

# color scheme available in ~/.config/qtile/themes
theme = "dracula"

theme_path = path.join(
    path.expanduser("~"), ".config", "qtile", "themes", theme
)

# map color name to hex values
with open(path.join(theme_path, "colors.json")) as f:
    colors = json.load(f)

img = {}


image_dimensions = dimensions(13, bar_dimensions.width)

# map img name to its path
img_path = path.join(theme_path, "img")
for i in listdir(img_path):
    img[i.split(".")[0]] = path.join(img_path, i)
