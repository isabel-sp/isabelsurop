from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def gauss(x, H, A, x0, sigma):
    return H + A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

def gauss_fit(x, y):
    mean = sum(x * y) / sum(y)
    sigma = np.sqrt(sum(y * (x - mean) ** 2) / sum(y))
    popt, pcov = curve_fit(gauss, x, y, p0=[min(y), max(y), mean, sigma])
    return popt


# generate simulated data
np.random.seed(123)  # comment out if you want different data each time
xdata = np.linspace(3, 10, 100)
ydata_perfect = gauss(xdata, 20, 5, 6, 1)
ydata = np.random.normal(ydata_perfect, 1, 100)

H, A, x0, sigma = gauss_fit(xdata, ydata)
FWHM = 2.35482 * sigma

print('The offset of the gaussian baseline is', H)
print('The center of the gaussian fit is', x0)
print('The sigma of the gaussian fit is', sigma)
print('The maximum intensity of the gaussian fit is', H + A)
print('The Amplitude of the gaussian fit is', A)
print('The FWHM of the gaussian fit is', FWHM)

plt.plot(xdata, ydata, 'ko', label='data')
plt.plot(xdata, ydata_perfect, '-k', label='data (without_noise)')
plt.plot(xdata, gauss(xdata, *gauss_fit(xdata, ydata)), '--r', label='fit')

plt.legend()
plt.title('Gaussian fit,  $f(x) = A e^{(-(x-x_0)^2/(2sigma^2))}$')
plt.xlabel('Motor position')
plt.ylabel('Intensity (A)')
plt.show()