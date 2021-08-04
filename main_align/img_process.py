
import numpy as np
from numpy.lib.function_base import average
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt

def bw_green(img):
    for row in img:
        for col in img[row]:
            img[row][col] = [img[row][col][1], img[row][col][1], img[row][col][1]]
    return img

def find_light_point(img, x, y, p = 10, scope = 50):

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

def findline_y(img, x, y, thickness = 3, h = 20):
    pixel_range = [img[y + y_shift][x] for y_shift in range(-h, h)]
    lowest = y - h + pixel_range.index(min(pixel_range))
    y1 = (x, lowest)

    #gets lower percentile of range (can be simplified with numpy)
    pixel_range = [img[y + y_shift][x] for y_shift in range(-5 * thickness, 5 * thickness)]
    pixel_range.sort()
    threshold = pixel_range[thickness]
    top_edge, bot_edge = (None, None)
    
    #can also be simplified -
    for y_shift in range(thickness):
        if img[y1 - y_shift][x] > threshold:
            top_edge = y1- y_shift
            break
    if top_edge == None: top_edge = y1 - thickness

    for y_shift in range(thickness):
        if img[y1+ y_shift][x] > threshold:
            bot_edge = y1 + y_shift
            break
    if bot_edge == None: bot_edge = y1 + thickness

    return (x, int((top_edge + bot_edge)/2))