import cv2 as cv2
import numpy as np
import math as math
import matplotlib.pyplot as plt


#y-centers click onto the minimum pixel value in a 200px range
def position_y(img, x, y, h = 20):
    pixel_range = [img[y + y_shift][x] for y_shift in range(-h, h)]
    lowest = y - h + pixel_range.index(min(pixel_range))
    return (x, lowest)

def line_center_y(img, x, y, thickness = 3):
    y1 = position_y(img, x, y)[1]
    pixel_range = [img[y + y_shift][x] for y_shift in range(-5 * thickness, 5 * thickness)]
    pixel_range.sort()
    threshold = pixel_range[thickness]
    top_edge, bot_edge = (None, None)

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

#x-centers click onto the minimum pixel value in a 200px range
def position_x(img, x, y, h = 100):
    pixel_range = [img[y][x + x_shift] for x_shift in range(-h, h)]
    plt.plot(pixel_range)
    plt.show(block = False)
    lowest = x - h + pixel_range.index(min(pixel_range))
    return (lowest, y)

def line_center_x(img, x, y, thickness = 10):
    x1 = position_x(img, x, y)[0]
    pixel_range = [img[y][x + x_shift] for x_shift in range(-5 * thickness, 5 * thickness)]
    plt.plot(pixel_range)
    plt.show(block = False)

    pixel_range.sort()
    threshold = pixel_range[thickness]
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

def line_center_x_light(img, x, y, thickness = 10):
    x1 = x
    pixel_range = [img[y][x + x_shift] for x_shift in range(-5 * thickness, 5 * thickness)]
    plt.plot(pixel_range)
    plt.show(block = False)

    pixel_range.sort()
    threshold = pixel_range[-1*thickness]
    r_edge, l_edge = (None, None)

    for x_shift in range(thickness):
        if img[y][x1 - x_shift] < threshold:
            r_edge = x1- x_shift
            break
    if r_edge == None: r_edge = x1 - thickness

    for x_shift in range(thickness):
        if img[y][x1+ x_shift] < threshold:
            l_edge = x1 + x_shift
            break
    if l_edge == None: l_edge = x1 + thickness

    return (int((r_edge + l_edge)/2), y)

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    i_out = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return i_out

def straighten(img, left, right):
    print((right[1] - left[1])/(right[0] - left[0]))
    angle = (180/math.pi) * (math.atan((right[1] - left[1])/(right[0] - left[0])))
    i_out = rotate_image(img, angle)
    return i_out


def x_pixels_plot(img, x, y):
    plt.plot(img[y])
    return



