# src/visualization/chart_style.py
"""
Shared matplotlib style for La Taxe Canicule.
Matches mauritan.site — white background, minimal color, clean typography.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl

# ── Palette ───────────────────────────────────────────────────────────────────
WHITE      = "#FFFFFF"
OFF_WHITE  = "#F8F8F8"
BLACK      = "#111111"
GREY_DARK  = "#444444"
GREY_MID   = "#888888"
GREY_LIGHT = "#DDDDDD"
RED        = "#C0392B"    # primary accent — heat
RED_LIGHT  = "#E8A090"    # secondary accent
SAND       = "#E8D5B0"    # neutral warm

def apply():
    """Apply global style."""
    mpl.rcParams.update({
        "figure.facecolor":     WHITE,
        "axes.facecolor":       WHITE,
        "axes.edgecolor":       GREY_LIGHT,
        "axes.labelcolor":      BLACK,
        "axes.titlecolor":      BLACK,
        "axes.spines.top":      False,
        "axes.spines.right":    False,
        "axes.grid":            True,
        "grid.color":           GREY_LIGHT,
        "grid.linewidth":       0.5,
        "grid.alpha":           0.8,
        "xtick.color":          GREY_DARK,
        "ytick.color":          GREY_DARK,
        "text.color":           BLACK,
        "font.family":          "serif",
        "font.size":            11,
        "axes.titlesize":       13,
        "axes.labelsize":       11,
        "figure.dpi":           150,
        "savefig.dpi":          150,
        "savefig.bbox":         "tight",
        "savefig.facecolor":    WHITE,
    })