# TimeBoss
Lightweight python timing class. Inspired by `TimeLord` (https://github.com/IceCubeOpenSource/skyllh)

## Installation
```
pip install TimeBoss
```

## Usage
```python
from time_boss import TimeBoss
import numpy as np

with TimeBoss("uniform and summary stats"):
    for i in range(100):
        a = np.random.uniform(10000)
        with TimeBoss("sum"):
            np.sum(a)
        with TimeBoss("mean"):
            np.average(a)

for i in range(100):
    with TimeBoss("normal"):
        a = np.random.normal(100000)

TimeBoss.result(unit="ms")
TimeBoss.plot_results()
```
