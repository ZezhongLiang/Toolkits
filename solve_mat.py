# -*- coding: utf-8 -*-

"""
                --------------------------------
                        >|<   Ekui Astro
                --------------------------------
                  Für den König, zu dem Licht!

solve_mat.py
This *.py file provides functions to solve matrix with greedy method.

@ Last updates: 2. Okt 2023
@ To-do: ok.
"""

import itertools
import os
import sys
from typing import Any

import numpy as np
import tqdm
from matplotlib import cm, colors
from matplotlib import pyplot as plt

try:
    import plot_style

    plt.rcParams.update(plot_style.RCPARAMS_UPDATE)
except ImportError as _:
    pass

# ---

# User preference
WIDTH = 10
HEIGHT = 16
TARGET_SUM = 10
MAX_SIZE = 15
FIGSIZE = (2.5, 5.0)


def pad_matrix(
    mat: np.ndarray, flags: np.ndarray, fill_value: Any
) -> np.ndarray:
    """
    pad_matrix function trims and pads matrix for display purposes.

    Args:
        mat (np.ndarray): matrix.
        flags (np.ndarray): flags array.
        fill_value (Any): fill value.

    Returns:
        np.ndarray: result.
    """

    for _i_start in range(mat.shape[0]):

        if not np.all(flags[_i_start]):
            break
    else:
        mat[:, :] = fill_value

        return mat

    for _i_end in range(mat.shape[0] - 1, 0, -1):

        if not np.all(flags[_i_end]):
            break

    for _j_start in range(mat.shape[1]):

        if not np.all(flags[:, _j_start]):
            break

    for _j_end in range(mat.shape[1] - 1, 0, -1):

        if not np.all(flags[:, _j_end]):
            break

    # Create a new, padded matrix
    mat_pad = np.full_like(mat, fill_value=fill_value, dtype=mat.dtype)
    mat_pad[_i_start : _i_end + 1, _j_start : _j_end + 1] = mat[
        _i_start : _i_end + 1, _j_start : _j_end + 1
    ]

    return mat_pad


def solve_matrix_single(mat: np.ndarray) -> np.ndarray:
    """
    solve_matrix_single function solves matrix with greedy method.

    Args:
        mat (np.ndarray): matrix.

    Returns:
        np.ndarray: summary of solution.
    """

    sub_mats = list()
    sub_mats_repr = list()

    # Check all possibilities
    for _i in range(HEIGHT):

        for _j in range(WIDTH):

            for _k in range(1, HEIGHT - _i + 1):

                for _l in range(1, WIDTH - _j + 1):

                    sub_sum = np.sum(mat[_i : _i + _k, _j : _j + _l])

                    if sub_sum == TARGET_SUM:

                        _sub_mat = np.full(
                            (HEIGHT, WIDTH),
                            dtype=np.bool_,
                            fill_value=np.False_,
                        )
                        _sub_mat[_i : _i + _k, _j : _j + _l] = np.True_

                        # Pad for display purposes
                        _sub_mat_repr = pad_matrix(
                            _sub_mat, (~_sub_mat | (mat == 0)), np.False_
                        )
                        _sub_mat[mat == 0] = np.False_

                        for _t in sub_mats:
                            if np.all(_t == _sub_mat):
                                break
                        else:
                            sub_mats_repr.append(_sub_mat_repr)
                            sub_mats.append(_sub_mat)

    # Detect overlappig possibilities
    ids_overlap_raw = list()
    ids_sub_mat_final = list()

    for (_i, _sub_mat) in enumerate(sub_mats):
        _ids_overlap = set()

        for (_j, _another) in enumerate(sub_mats):

            if _i == _j:
                continue

            if np.any(_sub_mat & _another):
                _ids_overlap.add(_j)

        if _ids_overlap:
            _ids_overlap.add(_i)
            ids_overlap_raw.append(_ids_overlap)
        else:
            # No overlap, add to final list
            ids_sub_mat_final.append(_i)

    # Group overlapping possibilities
    while True:
        ids_overlap_group = list()
        flag_ok = True

        # Connect overlapped groups iteratively
        for _ids_raw in ids_overlap_raw:

            for (_i, _ids_overlap) in enumerate(ids_overlap_group):

                if _ids_raw.intersection(_ids_overlap):
                    ids_overlap_group[_i] = _ids_overlap.union(_ids_raw)
                    flag_ok = False

                    break
            else:
                ids_overlap_group.append(_ids_raw)

        if flag_ok:
            break
        else:
            ids_overlap_raw = ids_overlap_group

    # Select the best option for each group
    for _ids_overlap in ids_overlap_group:

        _ids_overlap = list(_ids_overlap)
        (_ids_best, _yield_best) = (list(), 0)

        # If complexity is too high, rely on pure luck
        if len(_ids_overlap) > MAX_SIZE:
            np.random.shuffle(_ids_overlap)

            _ids_overlap = _ids_overlap[:MAX_SIZE]

        for _j in tqdm.tqdm(range(1, 2 ** len(_ids_overlap), 1)):
            _mats_sub_this = list()
            _ids_include = list()

            for _k in range(len(_ids_overlap)):
                _flag = (_j >> _k) & 1

                if _flag:
                    _mats_sub_this.append(sub_mats[_ids_overlap[_k]])
                    _ids_include.append(_ids_overlap[_k])

            # Consider if any included submatrices are overlapped
            if np.any(np.sum(_mats_sub_this, axis=0) > 1):

                continue
            elif np.sum(_mats_sub_this) > _yield_best:
                _ids_best = _ids_include

        ids_sub_mat_final.extend(_ids_best)

    # Generate summary for solution
    summary = np.zeros_like(mat, dtype=np.int64)

    for (_i, _id) in enumerate(ids_sub_mat_final, 1):

        summary[sub_mats_repr[_id]] = (
            _i * sub_mats_repr[_id][sub_mats_repr[_id]]
        )

    summary = summary.astype(np.float_)
    summary[summary == 0.0] = np.nan

    return summary


def plot_figure(mat: np.ndarray, summary: np.ndarray | None) -> int:
    """
    plot_figure function visualises results.

    Args:
        mat (np.ndarray): matrix.
        summary (np.ndarray | None): summary for solution.

    Returns:
        int: flag.
    """

    fig = plt.figure(figsize=FIGSIZE)
    ax = plt.subplot(1, 1, 1)

    cmap_summary = cm.get_cmap('prism')
    cmap_arr = colors.ListedColormap(['w', 'lightgrey'])

    ax.imshow(~np.isfinite(mat) | mat == 0, cmap=cmap_arr, vmax=1.0, vmin=0.0)

    if summary is not None:
        ax.imshow(summary, cmap=cmap_summary)

    for (_i, _j) in itertools.product(range(16), range(10)):
        if mat[_i, _j] > 0:
            ax.text(_j, _i, mat[_i, _j], ha='center', va='center')

    # Set ticks and axes
    ax.set_xticks(list())
    ax.set_yticks(list())
    ax.set_xticks(np.arange(10) + 0.5, minor=True)
    ax.set_yticks(np.arange(16) + 0.5, minor=True)
    ax.grid(which='minor', c='lightgrey')

    return 0


# Main function
if __name__ == '__main__':

    try:
        filename = sys.argv[1]
    except IndexError as _:
        filename = './demo.txt'

    print('__main__: loading file, {}.'.format(os.path.abspath(filename)))

    # Load using numpy
    my_mat = np.loadtxt(filename, dtype=np.int64, delimiter=',')
    my_mat = my_mat.reshape((HEIGHT, WIDTH))

    for _i in itertools.count():

        print('__main__: step, {}.'.format(_i + 1))

        summary = solve_matrix_single(my_mat)
        plot_figure(my_mat, summary)

        if not np.nansum(summary):
            break
        else:
            my_mat[summary > 0.0] = 0

        plt.tight_layout()
        plt.title('Step, {}, Score, {}'.format(_i + 1, np.sum(my_mat == 0.0)))

        plt.show()

    print('__main__: cannot think of more solutions.')

# EOF
