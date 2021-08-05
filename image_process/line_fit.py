import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import polynomial as P
from scipy.signal import argrelextrema
from scipy.optimize import curve_fit
import math

img = cv2.imread('bw_img.png')
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#img[680][325]

def polynomial_plot(x, coeffs):
    o = len(coeffs)
    y = 0
    for i in range(o):
        y += coeffs[i]*x**i
    return y




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
    y = lst[bounds[0]:bounds[1]]

    return y
    



y = find_light_point(img, 680, 325)
x = [i for i in range(len(y))]
print(y)


def f1(x, a, b, c, d, e, f, g):
	return (a * x) + (b * x**2) + (c * x**3) + (d * x**4) + (e * x**5) + (f * x**6) + (g * math.sin(x**7))
 
def f2(x, f, g):
	return f * math.sin(x + g)
 

# curve fit
popt, _ = curve_fit(f1, x, y)
# summarize the parameter values
print(popt)
a, b, c, d, e, f, g= popt
# plot input vs output
plt.scatter(x, y)
# define a sequence of inputs between the smallest and largest known inputs
x_line = np.arange(min(x), max(x), 1)
# calculate the output for the range
y_line = f1(x_line, a, b, c, d, e, f, g)
# create a line plot for the mapping function
plt.plot(x_line, y_line, '--', color='red')
plt.show()
