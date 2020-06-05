from custom.theme import colors
from custom.theme import image_dimensions
from custom.theme import img
from custom.theme import img_path
from custom.theme import theme_path

from custom.utils import update_tag, update_style_tag

from functools import lru_cache
from libqtile.log_utils import ColorFormatter
import logging
import os
import re
import sys


logger = logging.getLogger(__name__)
formatter = ColorFormatter(
    "$RESET$COLOR%(asctime)s  $RESET$BOLD[$COLOR%(filename)s:%(funcName)s():%(lineno)d$RESET$BOLD] $COLOR$BOLD%(levelname)s$RESET %(message)s"
)

stream_h = logging.StreamHandler()
stream_h.setFormatter(formatter)


logger.addHandler(stream_h)
logger.setLevel(logging.INFO)


try:
    from cairosvg import svg2png

    # TODO: add ids to svg and edit tags through ids instead of directly indexing
    #       the lines
    def process_image(pattern, name, height, width):
        if not os.path.exists(pattern):
            logger.critical("Pattern does not exist!")
            return
        if not (m := re.match(r"^(bg-to-)?.+$", name)):
            logger.warning("'%s' is not a valid file name", name)
            return

        fg, bg = "#000000", "#000000"
        if m.group(1) is not None:
            g = m.group()
            g = g[len(m.group(1)):]
            print(g)
            fg, bg = colors[g], colors["dark"]
        else:
            fgn = m.group()
            bgn = "secondary" if fgn == "primary" else "primary"
            fg, bg = colors[fgn], colors[bgn]

        logger.debug("fg = %s, bg = %s", fg, bg)

        with open(pattern) as f:
            pat = f.read().split("\n")

        pat = [*filter(len, pat)]

        # Update dimensions
        pat[1] = update_tag(
            pat[1], {"height": height, "width": width}
        )
        logger.debug("Updated dimensions")
        # Foreground triangle
        pat[2] = update_style_tag(pat[2], {"fill": fg[0]})
        logger.debug("Updated background color")
        # Two Background triangles, because one big rect left borders and
        # i didn't like it.
        for i in (3, 4):
            pat[i] = update_style_tag(pat[i], {"fill": bg[0]})
        logger.debug("Updated foreground color")

        pat = "\n".join(pat)
        logger.info("Exporting image to \x1b[38;5;159m{}".format(os.path.join(img_path, name + '.png')))

        svg2png(bytestring=pat, write_to=os.path.join(
            img[name]))


except ImportError:
    logger.warning(
        "Not using on-time image production due to missing dependencies: cairosvg"
    )
    process_image = lambda *args: None
finally:

    @lru_cache
    def get(image_name, height=image_dimensions.height, width=image_dimensions.width):
        pattern = os.path.expandvars("$HOME/.config/qtile/themes/pattern.svg")
        if not os.path.exists(pattern):
            logger.critical("Pattern does not exist!")
        elif not os.path.exists(theme_path):
            logger.error("Can't get your theme configuration")
        else:
            process_image(pattern, image_name, height, width)
        return img[image_name]
