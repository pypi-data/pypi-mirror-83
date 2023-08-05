# -----------------------------------------------------------------------------
# Description:    Module containing functions for drawing pulse schemes and circuit diagrams using matplotlib.
# Repository:     https://gitlab.com/qblox/packages/software/quantify/
# Copyright (C) Qblox BV & Orange Quantum Systems Holding BV (2020)
# -----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches


def new_pulse_fig(figsize=None):
    """
    Open a new figure and configure it to plot pulse schemes.
    """
    fig, ax = plt.subplots(1, 1, figsize=figsize, frameon=False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_ticklabels([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    fig.patch.set_alpha(0)
    ax.axhline(0, color='0.75')

    return fig, ax


def new_pulse_subplot(fig, *args, **kwargs):
    """
    Add a new subplot configured for plotting pulse schemes to a figure.

    All `*args` and `**kwargs` are passed to fig.add_subplot.
    """
    ax = fig.add_subplot(*args, **kwargs)
    ax.axis('off')
    fig.subplots_adjust(bottom=0, top=1, left=0, right=1)
    ax.axhline(0, color='0.75')

    return ax


def mwPulse(ax, pos, y_offs=0, width=1.5, amp=1, label=None, phase=0, label_height=1.3, color='C0',
            modulation='normal', **plot_kws):
    """
    Draw a microwave pulse: Gaussian envelope with modulation.
    """
    x = np.linspace(pos, pos + width, 100)
    envPos = amp * np.exp(-(x - (pos + width / 2))**2 / (width / 4)**2)
    envNeg = -amp * np.exp(-(x - (pos + width / 2))**2 / (width / 4)**2)

    if modulation == 'normal':
        mod = envPos * np.sin(2 * np.pi * 3 / width * x + phase)
    elif modulation == 'high':
        mod = envPos * np.sin(5 * np.pi * 3 / width * x + phase)
    else:
        raise ValueError()

    ax.plot(x, envPos+y_offs, '--', color=color, **plot_kws)
    ax.plot(x, envNeg+y_offs, '--', color=color, **plot_kws)
    ax.plot(x, mod+y_offs, '-', color=color, **plot_kws)

    if label is not None:
        ax.text(pos + width / 2, label_height, label, horizontalalignment='right', color=color).set_clip_on(True)

    return pos + width


def fluxPulse(ax, pos, y_offs=0, width=2.5, s=.1, amp=1.5, label=None, label_height=1.7, color='C1', **plot_kws):
    """
    Draw a smooth flux pulse, where the rising and falling edges are given by
    Fermi-Dirac functions.
    s: smoothness of edge
    """
    x = np.linspace(pos, pos + width, 100)
    y = amp / ((np.exp(-(x - (pos + 5.5 * s)) / s) + 1) * (np.exp((x - (pos + width - 5.5 * s)) / s) + 1))

    ax.fill_between(x, y+y_offs, color=color, alpha=0.3)
    ax.plot(x, y+y_offs, color=color, **plot_kws)

    if label is not None:
        ax.text(pos + width / 2, label_height, label, horizontalalignment='center', color=color).set_clip_on(True)

    return pos + width


def ramZPulse(ax, pos, y_offs=0, width=2.5, s=0.1, amp=1.5, sep=1.5, color='C1'):
    """
    Draw a Ram-Z flux pulse, i.e. only part of the pulse is shaded, to indicate
    cutting off the pulse at some time.
    """
    xLeft = np.linspace(pos, pos + sep, 100)
    xRight = np.linspace(pos + sep, pos + width, 100)
    xFull = np.concatenate((xLeft, xRight))
    y = amp / ((np.exp(-(xFull - (pos + 5.5 * s)) / s) + 1) * (np.exp((xFull - (pos + width - 5.5 * s)) / s) + 1))
    yLeft = y[:len(xLeft)]

    ax.fill_between(xLeft, yLeft+y_offs, alpha=0.3, color=color, linewidth=0.0)
    ax.plot(xFull, y+y_offs, color=color)

    return pos + width


def interval(ax, start, stop, y_offs=0, height=1.5, label=None, label_height=None, vlines=True, color='k',
             arrowstyle='<|-|>', **plot_kws):
    """
    Draw an arrow to indicate an interval.
    """
    if label_height is None:
        label_height = height + 0.2

    arrow = matplotlib.patches.FancyArrowPatch(
        posA=(start, height+y_offs), posB=(stop, height+y_offs), arrowstyle=arrowstyle,
        color=color, mutation_scale=7, **plot_kws)
    ax.add_patch(arrow)

    if vlines:
        ax.plot([start, start], [0+y_offs, height+y_offs], '--', color=color, **plot_kws)
        ax.plot([stop, stop], [0+y_offs, height+y_offs], '--', color=color, **plot_kws)

    if label is not None:
        ax.text((start + stop) / 2, label_height+y_offs, label, color=color, ha='center').set_clip_on(True)


def meter(ax, x0, y0, y_offs=0, w=1.1, h=.8, color='black', fillcolor=None):
    """
    Draws a measurement meter on the specified position.
    """
    if fillcolor is None:
        fill = False
    else:
        fill = True
    p1 = matplotlib.patches.Rectangle(
        (x0-w/2, y0-h/2+y_offs), w, h, facecolor=fillcolor, edgecolor=color, fill=fill, zorder=5)
    ax.add_patch(p1)
    p0 = matplotlib.patches.Wedge(
        (x0, y0-h/1.75+y_offs), .4, theta1=40, theta2=180-40, color=color, lw=2, width=.01, zorder=5)
    ax.add_patch(p0)
    r0 = h/2.2
    ax.arrow(x0, y0-h/5+y_offs, dx=r0*np.cos(np.deg2rad(70)), dy=r0*np.sin(np.deg2rad(70)), width=.03, color=color,
             zorder=5)


def box_text(ax, x0, y0, text='', w=1.1, h=.8, color='black', fillcolor=None, textcolor='black', fontsize=None):
    """
    Draws a box filled with text at the specified position.
    """
    if fillcolor is None:
        fill = False
    else:
        fill = True
    p1 = matplotlib.patches.Rectangle((x0-w/2, y0-h/2), w, h, facecolor=fillcolor, edgecolor=color, fill=fill, zorder=5)
    ax.add_patch(p1)

    ax.text(x0, y0, text, ha='center', va='center', zorder=6, size=fontsize, color=textcolor).set_clip_on(True)
