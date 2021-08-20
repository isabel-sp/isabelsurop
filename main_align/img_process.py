
import numpy as np
from numpy.lib.function_base import average
from numpy.lib.type_check import imag
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.backend_bases import MouseButton



def narrow_down(img, x, y, p = 20, scope = 75):

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
    bounds = (low or x-scope, high or x+scope)
    return (np.arange(bounds[0], bounds[1], 1), lst[bounds[0]:bounds[1]])


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


def max_list(data):
    try:
        return data.index(max(data))
    except:
        return None


def onclick(event):
    global ix, iy
    global fig
    ix, iy = event.xdata, event.ydata
    print ('x = %d, y = %d'%(
        ix, iy))

    global range_coords
    range_coords.append(int(ix))

    if event.button is MouseButton.RIGHT:
        fig.canvas.mpl_disconnect(cid)
        plt.close('range select (right click to set bounds)')
    
    if event.dblclick:
        range_coords = None
        fig.canvas.mpl_disconnect(cid)
        plt.close('range select (right click to set bounds)')

    return range_coords


def range_select(data):
    global fig
    global cid
    global range_coords

    range_coords = []

    x = data[0]
    y = data[1]
    shift = x[0]

    fig = plt.figure('range select (right click to set bounds)')
    plt.title('click on lower bound then upper bound, right click to set')
    plt.suptitle('double click to zoom out')
    plt.plot(x, y)
    
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    if range_coords == None or len(range_coords) < 3:
        return None

    start = range_coords[-3]
    end = range_coords[-2]

    return (np.arange(start, end, 1), y[start-shift:end-shift])


def gauss(x, H, A, x0, sigma):
    return H + A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))


def gauss_fit(x, y):
    mean = sum(x * y) / sum(y)
    sigma = np.sqrt(sum(y * (x - mean) ** 2) / sum(y))
    popt, pcov = curve_fit(gauss, x, y, p0=[min(y), max(y), mean, sigma])
    return popt


def gauss_fit_data(data):
    x, y = data
    H, A, x0, sigma = gauss_fit(x, y)
    FWHM = 2.35482 * sigma
    gauss_x = np.arange(x[0], x[-1], 0.1)

    # print('The offset of the gaussian baseline is', H)
    # print('The center of the gaussian fit is', x0)
    # print('The sigma of the gaussian fit is', sigma)
    # print('The maximum intensity of the gaussian fit is', H + A)
    # print('The Amplitude of the gaussian fit is', A)
    # print('The FWHM of the gaussian fit is', FWHM)

    plt.figure()
    plt.plot(x, y, 'ko', label='data')
    plt.plot(gauss_x, gauss(gauss_x, H, A, x0, sigma), '--r', label='fit')

    plt.legend()
    plt.title('Gaussian fit,  $f(x) = A e^{(-(x-x_0)^2/(2sigma^2))}$')
    plt.xlabel('position')
    plt.ylabel('Pixel Intensity')
    plt.show(block = False)

    return int(x0)


def find_snspd(image, x_selected, y_selected):
    
    narrow_data = narrow_down(image, x_selected, y_selected)
    if len(narrow_data) < 5:
        narrow_data = (np.arange(x_selected-50, x_selected+50, 1), image[y_selected][x_selected-100 : x_selected+100])
    selected_data = range_select(narrow_data)
    if selected_data == None:
        all_data = (np.arange(0, len(image[y_selected]), 1), image[y_selected])
        selected_data = range_select(all_data)
    
    try:
        x_found = gauss_fit_data(selected_data)
    except:
        print('something went wrong')
        x_found = max_list(selected_data)

    return (x_found or x_selected, y_selected)


if __name__ == ("__main__"):
    data = range_select(([3, 4, 5, 6, 7, 8, 9], [3, 4, 5, 6, 5, 4, 3]))
    print(data)
    print(gauss_fit_data(data))