"""Figure style for the empirical companion.

Values mirror ``.house-style/plot_style.py`` in the parent repository. They are
duplicated here rather than imported so the analysis package reproduces on its
own, which the companion's README promises.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

COLORS = {
    "primary": "#2E5077",
    "secondary": "#E85D4C",
    "tertiary": "#4DA375",
    "quaternary": "#9B6B9E",
    "quinary": "#D4A03E",
    "light": "#E8E8E8",
    "dark": "#2D2D2D",
    "accent": "#6AADE4",
}

CYCLE = [COLORS[k] for k in ("primary", "secondary", "tertiary", "quaternary", "quinary", "accent")]


def setup(font_size: float = 9.0, title_size: float = 10.0, tick_size: float = 8.0) -> None:
    """Apply the house figure style."""
    plt.rcParams.update({
        "figure.facecolor": "white",
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "font.family": "serif",
        "font.serif": ["EB Garamond", "Garamond", "Georgia", "Times New Roman"],
        "font.size": font_size,
        "axes.titlesize": title_size,
        "axes.labelsize": font_size,
        "xtick.labelsize": tick_size,
        "ytick.labelsize": tick_size,
        "legend.fontsize": tick_size,
        "axes.facecolor": "white",
        # EB Garamond has no U+2212, so negative ticks would render as a
        # missing-glyph box. Fall back to the ASCII hyphen.
        "axes.unicode_minus": False,
        "axes.edgecolor": COLORS["dark"],
        "axes.linewidth": 0.8,
        "axes.grid": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": plt.cycler("color", CYCLE),
        "xtick.direction": "out",
        "ytick.direction": "out",
        "legend.frameon": False,
        "lines.linewidth": 1.5,
    })
