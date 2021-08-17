import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def onclick(event):
    global ix, iy
    global fig
    ix, iy = event.xdata, event.ydata
    print ('x = %d, y = %d'%(
        ix, iy))

    global range_coords
    range_coords.append(int(ix))

    if event.dblclick:
        fig.canvas.mpl_disconnect(cid)
        plt.close('range select (double click to set)')

    return range_coords


def range_select(data):
    global fig
    global cid
    global range_coords

    range_coords = []

    x = data[0]
    y = data[1]
    shift = x[0]

    fig = plt.figure('range select (double click to set)')
    ax = fig.add_subplot(111)
    ax.plot(x, y)
    

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    start = range_coords[-4]
    end = range_coords[-3]

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

    print('The offset of the gaussian baseline is', H)
    print('The center of the gaussian fit is', x0)
    print('The sigma of the gaussian fit is', sigma)
    print('The maximum intensity of the gaussian fit is', H + A)
    print('The Amplitude of the gaussian fit is', A)
    print('The FWHM of the gaussian fit is', FWHM)

    plt.figure()
    plt.plot(x, y, 'ko', label='data')
    plt.plot(gauss_x, gauss(gauss_x, H, A, x0, sigma), '--r', label='fit')

    plt.legend()
    plt.title('Gaussian fit,  $f(x) = A e^{(-(x-x_0)^2/(2sigma^2))}$')
    plt.xlabel('position')
    plt.ylabel('Pixel Intensity')
    plt.show()

    return x0


if __name__ == ("__main__"):
    data = range_select(([3, 4, 5, 6, 7, 8, 9], [3, 4, 5, 6, 5, 4, 3]))
    print(data)
    print(gauss_fit_data(data))