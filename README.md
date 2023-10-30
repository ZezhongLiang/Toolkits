# Toolkits
Toolkits for generic purposes related to astronomical data reduction and analysis.

## Change log: 30. Okt 2023

* Update: `solve_mat.py`, iterative search method is now added.

## Change log: 28. Okt 2023

* Update: `solve_mat.py`, fix known issues regarding size.
  
## Change log: 27. Okt 2023

* Add: `solve_mat.py`. This `*.py` file solves matrix puzzle using greedy method. Save the matrix puzzle you want to solve as comma-separated-values (CSV) in a `txt` file, e.g.

<pre>
8,6,6,2,3,8,7,7,3,5,9,8,3,5,7,4,5,7,7,8,4,3,4,9,7,5,2,4,3,7,2,4,5,6,4,3,7,8,1,9,8,1,2,6,5,9,2,5,1,1,3,2,1,9,3,8,9,4,8,2,2,8,3,7,5,9,2,3,3,5,6,1,6,9,6,8,6,5,5,5,2,4,1,7,2,8,4,5,9,2,1,9,8,7,1,6,8,6,3,1,7,1,3,2,7,5,9,3,9,8,3,2,5,6,7,8,1,6,8,3,9,9,5,3,7,6,7,8,9,9,9,2,2,2,3,2,9,2,1,9,5,6,7,7,2,9,5,2,4,9,6,5,8,2,3,7,3,8,3,3
</pre>

save the `txt` file as `demo.txt` under the same working directory as the code. In console, input

<pre class="bash">
cd &lt;your_working_directory&gt;
python ./solve_mat.py
</pre>

and observe the result.

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
