from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import csv


def gauss(x, H, A, x0, sigma):
    return H + A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

def gauss_fit(x, y):
    mean = sum(x * y) / sum(y)
    sigma = np.sqrt(sum(y * (x - mean) ** 2) / sum(y))
    popt, pcov = curve_fit(gauss, x, y, p0=[min(y), max(y), mean, sigma])
    return popt

def gauss_fit_data(data):
    ydata = data
    xdata = np.linspace(0, len(data), len(data))
    H, A, x0, sigma = gauss_fit(xdata, ydata)
    FWHM = 2.35482 * sigma

    print('The offset of the gaussian baseline is', H)
    print('The center of the gaussian fit is', x0)
    print('The sigma of the gaussian fit is', sigma)
    print('The maximum intensity of the gaussian fit is', H + A)
    print('The Amplitude of the gaussian fit is', A)
    print('The FWHM of the gaussian fit is', FWHM)

    plt.figure()
    plt.plot(xdata, ydata, 'ko', label='data')
    plt.plot(xdata, gauss(xdata, *gauss_fit(xdata, ydata)), '--r', label='fit')

    plt.legend()
    plt.title('Gaussian fit,  $f(x) = A e^{(-(x-x_0)^2/(2sigma^2))}$')
    plt.xlabel('position')
    plt.ylabel('Pixel Intensity')
    plt.show()

    return x0


if __name__ == "__main__":
    with open('GFG', 'rU') as f:
        data = [[int(x) for x in rec] for rec in csv.reader(f, delimiter=',')]

    ydata = data[0][134:143]
    xdata = np.linspace(134, 143, 9)
    gauss_fit_data(ydata)