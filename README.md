# Toolkits
Toolkits for generic purposes related to astronomical data reduction and analysis.

## Change log: 3. Juli 2023

* Add: `yoshida_4_1990.py`. This `*.py` file implements 4-th-order Yoshida algorithm for integration of equation of motion. This algorithm is simple but symplectic. As an example, we define a force field corresponding to a galaxy whose rotation curve is flat.

<pre class="python">
def flat_rc(x, v, *args, **kwargs):
    return -x * 1.0 / np.sum(np.square(x))
</pre>

Any mass-point orbiting the potential centre with velocity vector along the azimuthal direction and length $v=1$ should therefore trace a circular orbit. Now implement the integration numerically and observe the results.

<pre class="python">
results = yoshida_4_1990.motion_solver(
    method=yoshida_4_1990.yoshida_4,
    acc=flat_rc,
    pos_0=np.array([10.0, 0.0]),
    vel_0=np.array([0.0, 1.0]),
    t_0=0.0,
    dt=0.01,
    t_max=1000.0,
)

x0s = [_o[1][0] for _o in results]
y0s = [_o[1][-1] for _o in results]
</pre>

## Change log: 20. Juni 2023

* Add: `plot_style.py`. This `*.py` file is used to set plot styles. Use as follows.

<pre>
from matplotlib.pyplot import rcParams
import plot_style

rcParams.update(plot_style.RCPARAMS_UPDATE)
</pre>

## Change log: 23. Mär 2023

* Add: `noise_sigma.py`. This `*.py` file is used to add noise to image and generate corresponding sigma-map.
