'''
Main file to run to align
'''

from windows_setup import configure_path
configure_path()


import cv2
import time
import numpy as np
from cam_helper import *
from display_functions import *
from img_process import *
from piezo_helper import *
from straighten import straighten_sequence
from datetime import datetime

raw_img = None
bw_img = None
color_img = np.zeros((1080,1440 ,3), np.uint8)
temp_clicked = None
snspd = None
wvguide = None
angle = 0
img_save_num = 10
pzt = PZT_driver()



#CALLBACK FUNCTIONS
def raw_img_format(event, x, y, flags, param):
    global bw_img
    global color_img
    global angle
    global img_save_num

    if event == cv2.EVENT_LBUTTONDOWN:
        color_img = size_and_straighten(raw_img, angle or 0)
        bw_img = convert_green(color_img)
    
    if event == cv2.EVENT_RBUTTONDOWN:
        color_img = size_and_straighten(raw_img, angle or 0)
        bw_img = convert_bw(color_img)
        #cv2.imwrite("C:\Users\Experiment\Documents\Isabel UROP\isabelsurop\all_images\colorimg{num}.png".format(num = str(img_save_num)), color_img)
        now = datetime.now()
        day = now.strftime("%d")
        image_prefix = now.strftime("%m_%d_%H_%M_%S")
        print(image_prefix)
        cv2.imwrite(image_prefix + '.png', color_img)
        img_save_num += 1

    
def main_click(event, x, y, flags, param):
    global bw_img
    global temp_clicked
    global snspd
    global wvguide
    global angle

    if event == cv2.EVENT_LBUTTONDOWN:
        print('clicked')
        click = button_clicked(x, y)
        if not click:
            print('marked point')
            #mark temporary point
            temp_clicked = (x, y)

        elif click == 'align' and snspd and wvguide:
            global pzt
            print('aligned')
            #RUN ALIGNMENT THING
            print('moving stage')
            stage_shift = wvguide[0] - snspd[0] #in estimated pixels??
            pzt.shift_pixel(stage_shift)
            print(pzt.y)

            time.sleep(2)
            
            print('stage moved x amount')

            #UPDATE CAPTURED IMAGE
            bw_img = cv2.cvtColor(raw_img,cv2.COLOR_BGR2GRAY)
            bw_img = cv2.resize(bw_img, (1440, 1080))

            #UPDATE VALUES
            temp_clicked = None
            x_found_wvguide = max_list(narrow_down(bw_img, temp_clicked[0], temp_clicked[1]))
            wvguide = (x_found_wvguide or temp_clicked[0], temp_clicked[1])

            #search estimated area that snspd shifted to
            snspd = find_snspd(bw_img, snspd[0] + stage_shift, snspd[1])

        elif click == 'straighten':
            angle = None
            print('angle setting')
            print(angle)
        
        elif click == 'stage':
            print('stage speed setting')

        elif not temp_clicked == None:
            print('setting value')
            if click == 'snspd':
                #take temp and try to find snspd waveguide, set coordinate
                snspd = find_snspd(bw_img, temp_clicked[0], temp_clicked[1])
                
            elif click == 'wvguide':
                #take temp and try to find waveguide, set coordinate
                x_found = max_list(narrow_down(bw_img, temp_clicked[0], temp_clicked[1]))
                wvguide = (x_found or temp_clicked[0], temp_clicked[1])

            temp_clicked = None
        else:
            print('click somewhere to set value')
        


#Open windows and detect clicks
cv2.namedWindow("Camera Feed")
cv2.namedWindow("Captured Image")
cv2.namedWindow("Controls")
cv2.resizeWindow("Controls", (1000, 50))
cv2.setMouseCallback("Camera Feed", raw_img_format)
cv2.setMouseCallback("Captured Image", main_click)
cv2.createTrackbar('Piezo Stage Speed', "Controls", 25, 50, pzt.set_ratio)

#Initialize Camera
image_feed = ImageAcquisition()

#Main image loop
while True:
    raw_img = image_feed.get_frame(raw_img)

    cv2.imshow('Camera Feed', raw_img)
    cv2.imshow("Captured Image", draw_buttons(color_img, temp_clicked, snspd, wvguide, pzt))

    if cv2.waitKey(1) & 0xFF == ord("q"):
        del image_feed
        cv2.destroyAllWindows()
    
    if angle == None:
        angle = straighten_sequence(bw_img)
        raw_img = size_and_straighten(raw_img, angle or 0)
        bw_img = convert_green(color_img)
        print('angle set')
        print(angle)

