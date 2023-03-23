# -*- coding: utf-8 -*-

"""
                --------------------------------
                        >|<   Ekui Astro
                --------------------------------
                  Für den König, zu dem Licht!

noise_sigma.py
This *.py file adds noise to model image and evaluates sigma-map.

@ Last updates: 23. Mär 2023
@ To-do: ok.
"""

import argparse
import os

import numpy as np
from astropy import time
from astropy.io import fits


def noise_sigma(
    im: np.ndarray, gain: float = 50.0, seed: int = 0
) -> tuple[np.ndarray, np.ndarray]:
    """
    noise_sigma function adds noise to model image and evaluates
    sigma-map.

    Args:
        im (np.ndarray): image.
        gain (float, optional): effective gain, in unit e-.adu^{-1}.
            Defaults to 50.0.
        seed (int, optional): seed to random number generator.
            Defaults to 0.

    Returns:
        tuple[np.ndarray, np.ndarray]: image with noise added and
            corresponding sigma-map.
    """

    rng = np.random.default_rng(seed=seed)

    im_noise = rng.poisson(im * gain) / gain
    im_sigma = np.sqrt(im * gain) / gain

    return (im_noise, im_sigma)


# Main function
if __name__ == '__main__':

    # Get argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='filename.', type=str)
    parser.add_argument('result_name', help='result filename.', type=str)
    parser.add_argument(
        '-s', '--sigma_name', default='', help='sigma filename.', type=str
    )
    parser.add_argument(
        '-g',
        '--gain',
        default=50.0,
        help='[e-.adu^{-1}] effective gain. Defaults to 50.0.',
        type=float,
    )
    parser.add_argument(
        '-S',
        '--seed',
        default=0,
        help='seed to random number generator. Defaults to 0.',
        type=int,
    )
    args = parser.parse_args()

    # Parse parameters
    filename = args.filename
    result_name = args.result_name
    sigma_name = args.sigma_name
    gain = args.gain
    seed = args.seed

    # Get image
    with fits.open(filename) as _h:
        im_data = _h[0].data.copy()
        header = _h[0].header.copy()

    # Get image with noise and sigma map
    (im_noise, im_sigma) = noise_sigma(im_data, gain=gain, seed=seed)

    header.update(
        {
            'comment': 'noise_sigma: created from, {}, at, {}.'.format(
                filename, time.Time.now().fits
            )
        }
    )

    # Save results to file
    fits.PrimaryHDU(header=header, data=im_noise).writeto(
        result_name, overwrite=True
    )

    if sigma_name:
        fits.PrimaryHDU(header=header, data=im_sigma).writeto(
            sigma_name, overwrite=True
        )

    print('noise_sigma: done.')

# EOF
