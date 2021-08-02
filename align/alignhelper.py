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

########################
def rotate_image(image, angle):

    # Get the image size
    image_size = (image.shape[1], image.shape[0])
    image_center = tuple(np.array(image_size) / 2)

    # Convert the OpenCV 3x2 rotation matrix to 3x3
    rot_mat = np.vstack(
        [cv2.getRotationMatrix2D(image_center, angle, 1.0), [0, 0, 1]]
    )

    rot_mat_notranslate = np.matrix(rot_mat[0:2, 0:2])

    # Shorthand for below calcs
    image_w2 = image_size[0] * 0.5
    image_h2 = image_size[1] * 0.5

    # Obtain the rotated coordinates of the image corners
    rotated_coords = [
        (np.array([-image_w2,  image_h2]) * rot_mat_notranslate).A[0],
        (np.array([ image_w2,  image_h2]) * rot_mat_notranslate).A[0],
        (np.array([-image_w2, -image_h2]) * rot_mat_notranslate).A[0],
        (np.array([ image_w2, -image_h2]) * rot_mat_notranslate).A[0]
    ]

    # Find the size of the new image
    x_coords = [pt[0] for pt in rotated_coords]
    x_pos = [x for x in x_coords if x > 0]
    x_neg = [x for x in x_coords if x < 0]

    y_coords = [pt[1] for pt in rotated_coords]
    y_pos = [y for y in y_coords if y > 0]
    y_neg = [y for y in y_coords if y < 0]

    right_bound = max(x_pos)
    left_bound = min(x_neg)
    top_bound = max(y_pos)
    bot_bound = min(y_neg)

    new_w = int(abs(right_bound - left_bound))
    new_h = int(abs(top_bound - bot_bound))

    # We require a translation matrix to keep the image centred
    trans_mat = np.matrix([
        [1, 0, int(new_w * 0.5 - image_w2)],
        [0, 1, int(new_h * 0.5 - image_h2)],
        [0, 0, 1]
    ])

    # Compute the tranform for the combined rotation and translation
    affine_mat = (np.matrix(trans_mat) * np.matrix(rot_mat))[0:2, :]

    # Apply the transform
    result = cv2.warpAffine(
        image,
        affine_mat,
        (new_w, new_h),
        flags=cv2.INTER_LINEAR
    )

    return result


def largest_rotated_rect(w, h, angle):
    """
    Given a rectangle of size wxh that has been rotated by 'angle' (in
    radians), computes the width and height of the largest possible
    axis-aligned rectangle within the rotated rectangle.

    Original JS code by 'Andri' and Magnus Hoff from Stack Overflow

    Converted to Python by Aaron Snoswell
    """

    quadrant = int(math.floor(angle / (math.pi / 2))) & 3
    sign_alpha = angle if ((quadrant & 1) == 0) else math.pi - angle
    alpha = (sign_alpha % math.pi + math.pi) % math.pi

    bb_w = w * math.cos(alpha) + h * math.sin(alpha)
    bb_h = w * math.sin(alpha) + h * math.cos(alpha)

    gamma = math.atan2(bb_w, bb_w) if (w < h) else math.atan2(bb_w, bb_w)

    delta = math.pi - alpha - gamma

    length = h if (w < h) else w

    d = length * math.cos(alpha)
    a = d * math.sin(alpha) / math.sin(delta)

    y = a * math.cos(gamma)
    x = y * math.tan(gamma)

    return (
        bb_w - 2 * x,
        bb_h - 2 * y
    )


def crop_around_center(image, width, height):
    """
    Given a NumPy / OpenCV 2 image, crops it to the given width and height,
    around it's centre point
    """

    image_size = (image.shape[1], image.shape[0])
    image_center = (int(image_size[0] * 0.5), int(image_size[1] * 0.5))

    if(width > image_size[0]):
        width = image_size[0]

    if(height > image_size[1]):
        height = image_size[1]

    x1 = int(image_center[0] - width * 0.5)
    x2 = int(image_center[0] + width * 0.5)
    y1 = int(image_center[1] - height * 0.5)
    y2 = int(image_center[1] + height * 0.5)

    return image[y1:y2, x1:x2]


def nice_rotate(img, angle):
    image_height, image_width = img.shape[0:2]
    rotated = rotate_image(np.copy(img), angle)
    return crop_around_center(rotated, *largest_rotated_rect(image_width, image_height,math.radians(angle)))
################################

def straighten(img, left, right):
    print((right[1] - left[1])/(right[0] - left[0]))
    angle = (180/math.pi) * (math.atan((right[1] - left[1])/(right[0] - left[0])))
    i_out = nice_rotate(img, angle)
    return i_out


def x_pixels_plot(img, x, y):
    plt.plot(img[y])
    return



