from numba import njit
import numpy as np

@njit
def opt_contains(ms_1, ms_2):
    aux_1 = np.array(ms_1, dtype=np.int32)
    aux_2 = np.array(ms_2, dtype=np.int32)
    for i in len(aux_2):
        if aux_2[i] > aux_1[i]:
            return False
    return True
    
@njit
def opt_sum(ms_1, ms_2):
    keys = set(list(ms_1.keys()) + list(ms_2.keys()))
    return {key: (ms_1.get(key, 0) + ms_2.get(key, 0)) for key in keys}
    
@njit
def opt_sub(ms_1, ms_2):
    keys = set(list(ms_1.keys()) + list(ms_2.keys()))
    return {key: max(ms_1.get(key, 0) + ms_2.get(key, 0), 0) for key in keys}