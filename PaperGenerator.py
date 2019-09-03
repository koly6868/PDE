import numpy as np
import random
def Generate(x_size : int,y_size : int, C : float, dis : float):
    res = np.zeros((x_size,y_size))
    for x in range(0,x_size):
        for y in range(0,y_size):
            res[x,y] = C + (2*random.random() - 1) * dis
    return res
