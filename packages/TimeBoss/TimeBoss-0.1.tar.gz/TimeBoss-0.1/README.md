# TimeBoss
Lightweight python timing class. Inspired by `TimeLord` (https://github.com/IceCubeOpenSource/skyllh)

## Usage
```python
from time_boss import TimeBoss
import numpy as np

with TimeBoss("root1"):
    for i in range(100):
        a = np.random.uniform(10000)
        with TimeBoss("sum"):
            np.sum(a)
        with TimeBoss("mean"):
            np.average(a)

with TimeBoss("root2"):
    a = np.random.normal(100000)

TimeBoss.result(unit="ms")
```
