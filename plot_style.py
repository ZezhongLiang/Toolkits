# -*- coding: utf-8 -*-

"""
                --------------------------------
                        >|<   Ekui Astro
                --------------------------------
                  Für den König, zu dem Licht!

plot_style.py
This *.py file provides plot styles.

@ Last updates: 20. Juni 2023
@ To-do: ok.
"""

from matplotlib import legend_handler, patheffects

# ---

# Rcparams configuration
RCPARAMS_UPDATE = {
    # Lines
    'lines.linewidth': 1.0,
    'lines.dash_capstyle': 'round',
    'lines.solid_capstyle': 'round',
    'lines.dashed_pattern': (5.0, 3.0),
    'lines.dashdot_pattern': (5.0, 3.0, 1.0, 3.0),
    'lines.dotted_pattern': (1.0, 3.0),
    # Patches
    'patch.linewidth': 1.0,
    # Hacthes
    'hatch.linewidth': 1.0,
    # Font
    'font.family': 'FreeSerif',
    # LaTeX
    'text.usetex': False,
    'mathtext.fontset': 'stix',
    # Axes
    'axes.facecolor': 'none',
    'axes.titlesize': 'medium',
    'axes.titleweight': 'bold',
    'axes.labelpad': 2.5,
    'axes.formatter.limits': (-3.9, 3.9),
    'axes.formatter.use_locale': True,
    'axes.formatter.use_mathtext': True,
    'axes.formatter.useoffset': True,
    # Ticks
    'xtick.top': True,
    'xtick.bottom': True,
    'xtick.major.size': 6.0,
    'xtick.minor.size': 4.0,
    'xtick.major.width': 1.0,
    'xtick.minor.width': 1.0,
    'xtick.major.pad': 2.5,
    'xtick.minor.pad': 2.5,
    'xtick.direction': 'in',
    'xtick.alignment': 'center',
    'ytick.left': True,
    'ytick.right': True,
    'ytick.major.size': 6.0,
    'ytick.minor.size': 4.0,
    'ytick.major.width': 1.0,
    'ytick.minor.width': 1.0,
    'ytick.major.pad': 2.5,
    'ytick.minor.pad': 2.5,
    'ytick.direction': 'in',
    'ytick.alignment': 'center',
    # Grids
    'grid.linewidth': 1.0,
    # Legend
    'legend.framealpha': 1.0,
    'legend.fancybox': False,
    'legend.facecolor': 'w',
    'legend.edgecolor': 'none',
    'legend.labelspacing': 0.25,
    'legend.handletextpad': 0.5,
    'legend.columnspacing': 0.5,
    # Figure
    'figure.dpi': 100,
    'figure.autolayout': True,
    # Images
    'image.origin': 'lower',
    'image.lut': 1024,
    # Errorbar plots
    'errorbar.capsize': 3.0,
    # Saving figures
    'savefig.dpi': 300,
}

# Handler map used for creating legend handlers
HANDLER_MAP = {
    list: legend_handler.HandlerTuple(ndivide=None),
    tuple: legend_handler.HandlerTuple(),
}

# Path effects
PATH_EFFECTS_1 = [
    patheffects.Stroke(linewidth=3.0, foreground='w'),
    patheffects.Normal(),
]
PATH_EFFECTS_3 = [
    patheffects.Stroke(linewidth=7.0, foreground='w'),
    patheffects.Normal(),
]

# EOF
