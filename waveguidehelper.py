import numpy as np

def narrow_down(lst, x, p, scope):
    #lst = np.ndarray.tolist(lst)
    cut = int(len(lst)*((100-scope)/200))
    cutoff = np.percentile(lst[cut:-cut], p)
    low = None
    high = None
    print(lst[x] > cutoff)
    for shift in range(len(lst)//2):
        if (lst[x-shift] > cutoff).any() and (low == None):
            low = x-shift
        if (lst[x+shift] > cutoff).any() and (high == None):
            high = x+shift
    return(low or x, high or x)
    