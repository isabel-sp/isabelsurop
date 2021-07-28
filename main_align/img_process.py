
import numpy as np
from numpy.lib.function_base import average
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt

def bw_green(img):
    for row in img:
        for col in img[row]:
            img[row][col] = [img[row][col][1], img[row][col][1], img[row][col][1]]
    return img

def temp_findline(row, x, p = 10, scope = 50):
    print(row)
    cut = int(len(row)*((100-scope)/200))
    cutoff = np.percentile(row[cut:-cut], p)
    low = None
    high = None
    print(row[x] > cutoff)
    for shift in range(len(row)//2):
        if (row[x-shift] > cutoff).any() and (low == None):
            low = x-shift
        if (row[x+shift] > cutoff).any() and (high == None):
            high = x+shift
    bounds = (low or x, high or x)
    return average(bounds)

######################

def find_light_point(img, x, y, p = 10, scope = 50):
    #lst = np.ndarray.tolist(lst)
    lst = img[y]
    cut = int(len(lst)*((100-scope)/200))
    cutoff = np.percentile(lst[cut:-cut], p)
    low = None
    high = None

    for shift in range(len(lst)//2):
        if (x-shift > 0) and (lst[x-shift] > cutoff).any() and (low == None):
            low = x-shift
        if (x+shift < len(lst)) and (lst[x+shift] > cutoff).any() and (high == None):
            high = x+shift
    bounds = (low or x, high or x)
    local_max = argrelextrema(lst[bounds[0]:bounds[1]], np.greater)
    plt.figure()
    markers_on = local_max[0]
    plt.plot(lst[bounds[0]:bounds[1]], '-g.', mfc='red', mec='k', markevery=markers_on)
    plt.show(block = False)

    if len(local_max[0]) == 0:
        return None
    return local_max[0][0] + low


######################################OLD#################################
def position_x(img, x, y, h = 100):
    pixel_range = [img[y][x + x_shift] for x_shift in range(-h, h)]
    lowest = x - h + pixel_range.index(min(pixel_range))
    return (lowest, y)

def line_center_x(img, x, y, thickness = 50, percentile = 30):
    #x1 = position_x(img, x, y)[0]
    x1 = x
    # pixel_range = [img[y][x + x_shift] for x_shift in range(-5 * thickness, 5 * thickness)]
    # pixel_range.sort()
    # threshold = pixel_range[thickness]

    threshold = np.percentile(img[y][x-thickness:x+thickness], percentile)
    r_edge, l_edge = (None, None)

    for x_shift in range(thickness):
        if img[y][x1 - x_shift] > threshold:
            r_edge = x1- x_shift
            break
    if r_edge == None: r_edge = x1 - thickness

    for x_shift in range(thickness):
        if img[y][x1+ x_shift] > threshold:
            l_edge = x1 + x_shift
            break
    if l_edge == None: l_edge = x1 + thickness

    return (int((r_edge + l_edge)/2), y)