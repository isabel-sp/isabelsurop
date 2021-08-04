
import cv2
from display_functions import size_and_straighten
from img_process import bw_green
import math

output_y_coords = []
angle = 0

def findline_y(img, x, y, thickness = 3, h = 20):
    pixel_range = [img[y + y_shift][x] for y_shift in range(-h, h)]
    lowest = y - h + pixel_range.index(min(pixel_range))
    y1 = lowest

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


def get_angle(img, left, right):
    return (180/math.pi) * (math.atan((right[1] - left[1])/(right[0] - left[0])))


def img_click(event, x, y, flags, param):
    global output_y_coords
    global angle
    img = param[0]

    if event == cv2.EVENT_LBUTTONDOWN:
        center = findline_y(img, x, y, 20)
        output_y_coords.append(center)

        #stamp dots on image
        cv2.circle(img, (x,y), radius=2, color=(0, 0, 255), thickness=1)
        cv2.circle(img, center, radius=2, color=(0, 255, 255), thickness=1)
    
    #right click: straighten image based on last 2 clicks
    if event == cv2.EVENT_RBUTTONDOWN:
        angle = get_angle(img, output_y_coords[-1], output_y_coords[-2])
        print(angle)
        img = size_and_straighten(img, angle)


def straighten_sequence(img):
    global angle

    cv2.namedWindow('Straighten')
    cv2.setMouseCallback('Straighten', img_click, param = [img])

    while True:
        cv2.imshow('Straighten', img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyWindow('Straighten')

    return angle


if __name__ == '__main__':
    img_raw = cv2.imread('3clicked.png')
    img = cv2.cvtColor(img_raw,cv2.COLOR_BGR2GRAY)
    straighten_sequence(img)