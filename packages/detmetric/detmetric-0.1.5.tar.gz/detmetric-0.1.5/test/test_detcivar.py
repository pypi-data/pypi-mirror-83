from detcivar import DetStatic

precision = [0.1,0.2,0.3,0.4,0.5]


# test mean
p_mean = DetStatic().mu(precision)
print(p_mean)

real_mean = sum(precision) / len(precision)
print(real_mean)


# test variance

p_var = DetStatic().variance(precision)
print(p_var)

real_var = float((0.1-real_mean)**2 + (0.2-real_mean)**2  + (0.3-real_mean)**2  + (0.4-real_mean)**2  + (0.5-real_mean)**2) / (len(precision)-1)
print(real_var)

# test confidence

ci = DetStatic().detcivar(precision,level=0.95)

import pprint
pprint.pprint(ci)


# real
# N(0,1) 0.025 quntile like equel -1.9599639845400545
import numpy as np
lower = 0.3 - np.sqrt(0.025) / np.sqrt(5) * 1.9599639845400545
upper = 0.3 + np.sqrt(0.025) / np.sqrt(5) * 1.9599639845400545

print(lower)
print(upper)


# test done!!!

# 0.3
# 0.3
# 0.025
# 0.025
# {'CI': [0.16141, 0.43859], 'Var': 0.025}
# 0.16140961756503217
# 0.43859038243496784
