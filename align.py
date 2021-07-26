
# importing the module
import cv2
import numpy as np
import alignhelper as im
# import stagecontrol as mdt
import matplotlib.pyplot as plt

image_number = 0
output_y_coords = []
straightened = False

#initialize images, set bw and straight to empty
img_raw = cv2.imread('3clicked.png')

print(img_raw.shape)
print(img_raw)

img_bw = np.zeros((512,512,3), np.uint8)
img_straight = np.zeros((512,512,3), np.uint8)


#Mouse callback commands
def raw_img_click(event, x, y, flags, param):
    global img_bw

    #left click: update image, then also update black and white image
    if event == cv2.EVENT_LBUTTONDOWN:
        #UPDATE IMAGE CODE

        #update bw image
        img_bw = cv2.cvtColor(img_raw,cv2.COLOR_BGR2GRAY)
        img_bw = cv2.resize(img_bw, (640, 480))

def bw_img_click(event, x, y, flags, param):
    global output_y_coords
    global img_straight

    #left clicks: detect and center on horizonal lines, record coords
    if event == cv2.EVENT_LBUTTONDOWN:
        center = im.line_center_y(img_bw, x, y, 20)
        output_y_coords.append(center)

        #stamp dots on image
        cv2.circle(img_bw, (x,y), radius=2, color=(0, 0, 255), thickness=1)
        cv2.circle(img_bw, center, radius=2, color=(0, 255, 255), thickness=1)
    
    #right click: straighten image based on last 2 clicks
    if event == cv2.EVENT_RBUTTONDOWN:
        img_straight = im.straighten(img_bw, output_y_coords[-1], output_y_coords[-2])
        #img_straight = cv2.bitwise_not(img_straight)

def straight_img_click(event, x, y, flags, param):

    #left click, find coordinate of center waveguide
    if event == cv2.EVENT_LBUTTONDOWN:
        #print(img_straight)
        #center = im.line_center_x(img_straight, x, y, 20)
        #center = im.line_center_x_light(img_straight, x, y, 20)
        #cv2.circle(img_straight, center, radius=2, color=(0, 255, 255), thickness=1)
        plt.plot(img_straight[y])
        plt.show(block = False)

        # cv2.circle(img_straight, (center[0]+200, center[1]), radius=2, color=(0, 255, 255), thickness=1)
        # cv2.circle(img_straight, (center[0]-200, center[1]), radius=2, color=(0, 255, 255), thickness=1)
        #print("x coordinate of the waveguide is" + str(center[0]))


#Open windows
cv2.namedWindow("Raw Image")
cv2.namedWindow("BW Image")
cv2.namedWindow("Straight Image")

#Detect clicks
cv2.setMouseCallback("Raw Image", raw_img_click)
cv2.setMouseCallback("BW Image", bw_img_click)
cv2.setMouseCallback("Straight Image", straight_img_click)

while True:
    cv2.imshow("Raw Image", img_raw)
    cv2.imshow("BW Image", img_bw)
    cv2.imshow("Straight Image", img_straight)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cv2.destroyAllWindows()

#move on to shifting procedure


cv2.namedWindow("hello") 
cv2.waitKey(0)
cv2.destroyAllWindows()