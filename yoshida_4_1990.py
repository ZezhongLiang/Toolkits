# -*- coding: utf-8 -*-

"""
                --------------------------------
                        >|<   Ekui Astro
                --------------------------------
                  Für den König, zu dem Licht!

yoshida_4_1990.py
This *.py file provides the 4-th order motion integration algorithm
as is described by Yoshida (1990). The algorithm is symplectic.

@ Last updates: 3. Juli 2023
@ To-do: ok.
"""

import warnings
from collections.abc import Callable

import numpy as np
import tqdm

# ---

# Constants for 4-th order yoshida integrator (Yoshida, 1990)
C_1 = 1.0 / (2.0 * (2.0 - np.power(2.0, 1.0 / 3.0)))
C_2 = (1.0 - np.power(2.0, 1.0 / 3.0)) / (
    2.0 * (2.0 - np.power(2.0, 1.0 / 3.0))
)
C_3 = (1.0 - np.power(2.0, 1.0 / 3.0)) / (
    2.0 * (2.0 - np.power(2.0, 1.0 / 3.0))
)
C_4 = 1.0 / (2.0 * (2.0 - np.power(2.0, 1.0 / 3.0)))

D_1 = 1.0 / (2.0 - np.power(2.0, 1.0 / 3.0))
D_2 = -np.power(2.0, 1.0 / 3.0) / (2.0 - np.power(2.0, 1.0 / 3.0))
D_3 = 1.0 / (2.0 - np.power(2.0, 1.0 / 3.0))


def motion_solver(
    method: Callable,
    acc: Callable,
    pos_0: float = 0.0,
    vel_0: float = 0.0,
    t_0: float = 0.0,
    dt: float = 0.01,
    t_max: float = 1.0,
    stop: Callable = None,
    **kw_args
) -> list[tuple[float, np.ndarray | float, np.ndarray | float]]:
    """
    motion_solver function solves dimensionless equation of motion.

    Args:
        method (Callable): method for single-step integration.
            Callable object `method` should be declared in the form of
            `method(acc, pos, vel, t, dt, ...)` returning a tuple in
            form of `(pos, vel)`.
        acc (Callable): acceleration of equation of motion.
            Callable object `acc` should be defined in the form of
            `acc(pos, vel, t, ...)`, returning an acceleration vector.
        pos_0 (np.ndarray | float, optional): initial condition for
            position vector. Defaults to 0.0.
        vel_0 (np.ndarray | float, optional): initial condition for
            velocity vector. Defaults to 0.0.
        t_0 (float, optional): initial time. Defaults to 0.0.
        dt (float, optional): step length of single-step integration.
            Defaults to 0.01.
        t_max (float, optional): maximum time to evaluate.
            Defaults to 1.0.
        stop (Callable, optional): condition to stop. Defaults to None.

    Returns:
        list[tuple[float, np.ndarray | float, np.ndarray | float]]:
        times, position vectors, velocity vectors at each snapshot.
    """

    results = [(t_0, pos_0, vel_0)]
    _times = np.arange(t_0, t_max + dt, dt)

    if not isinstance(stop, Callable):

        for _t in tqdm.tqdm(_times):
            (_pos_next, _vel_next) = method(
                acc=acc,
                pos=results[-1][1],
                vel=results[-1][-1],
                t=_t,
                dt=dt,
                **kw_args
            )
            results.append((_t, _pos_next, _vel_next))
    else:

        for _t in _times:

            if stop(results[-1][1], results[-1][-1], _t, dt, **kw_args):
                break

            (_pos_next, _vel_next) = method(
                acc=acc,
                pos=results[-1][1],
                vel=results[-1][-1],
                t=_t,
                dt=dt,
                **kw_args
            )
            results.append((_t, _pos_next, _vel_next))
        else:

            warnings.warn(
                'solver: stop condition is not fufilled during the entire run.'
            )

    return results


def yoshida_4(
    acc: Callable,
    pos: np.ndarray,
    vel: np.ndarray,
    t: float,
    dt: float,
    **kw_args_acc
) -> tuple[np.ndarray | float, np.ndarray | float]:
    """
    yoshida_4 function returns single-step integration of dimensionless
    equation of motion utilising 4-th-order Yoshida integrator.

    Args:
        acc (Callable): acceleration vector of equation of motion.
            Callable `acc` should be defined in form of
            `acc(pos, vel, t, ...)` returning an acceleration vector.
        pos (np.ndarray | float): position vector.
        vel (np.ndarray | float): velocity vector.
        t (float): time.
        dt (float): step length of single-step integration.

    Returns:
        tuple[np.ndarray | float, np.ndarray | float]: position vector,
        velocity vector.
    """

    # See Yoshida (1990) for details
    x_1 = pos + C_1 * vel * dt
    v_1 = vel + D_1 * acc(x_1, vel, t, **kw_args_acc) * dt
    x_2 = x_1 + C_2 * v_1 * dt
    v_2 = v_1 + D_2 * acc(x_2, v_1, t, **kw_args_acc) * dt
    x_3 = x_2 + C_3 * v_2 * dt

    v_tdt = v_2 + D_3 * acc(x_3, v_2, t, **kw_args_acc) * dt
    x_tdt = x_3 + C_4 * v_tdt * dt

    return (x_tdt, v_tdt)


# EOF
