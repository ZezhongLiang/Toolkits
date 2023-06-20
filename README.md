# Toolkits
Toolkits for generic purposes related to astronomical data reduction and analysis.

## Change log: 20. Juni 2023

* Add: `plot_style.py`. This `*.py` file is used to set plot styles. Use as follows.

<pre>
from matplotlib.pyplot import rcParams
import plot_style

rcParams.update(plot_style.RCPARAMS_UPDATE)
</pre>

## Change log: 23. Mär 2023

* Add: `noise_sigma.py`. This `*.py` file is used to add noise to image and generate corresponding sigma-map.
