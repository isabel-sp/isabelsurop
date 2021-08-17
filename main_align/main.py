'''
Main file to run to align
'''

from align.gaussian_test import gauss_fit_data
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
from datetime import date, datetime
from data_range import range_select

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
        bw_img = img_process_bw(color_img)
    
    if event == cv2.EVENT_RBUTTONDOWN:
        color_img = size_and_straighten(raw_img, angle or 0)
        bw_img = img_process_bw(color_img)
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
            x_found_wvguide = find_light_point(bw_img, wvguide[0], wvguide[1])
            wvguide = (x_found_wvguide, wvguide[1])
            #search estimated area that snspd shifted to
            x_found_snspd = find_light_point(bw_img, snspd[0] + stage_shift, snspd[1])
            snspd = (x_found_snspd, snspd[1])

        elif click == 'straighten':
            angle = None
            print('angle setting')
            print(angle)

        elif not temp_clicked == None:
            print('setting value')
            if click == 'snspd':
                #take temp and try to find snspd waveguide, set coordinate
                selected_data = range_select(narrow_down(bw_img, temp_clicked[0], temp_clicked[1]))
                try:
                    x_found = gauss_fit_data(selected_data)
                except:
                    print('something went wrong')
                    x_found = max_list(selected_data)

                # x_found = find_light_point(bw_img, temp_clicked[0], temp_clicked[1])
                snspd = (x_found or temp_clicked[0], temp_clicked[1])
                
            elif click == 'wvguide':
                #take temp and try to find waveguide, set coordinate
                x_found = find_light_point(bw_img, temp_clicked[0], temp_clicked[1])
                wvguide = (x_found or temp_clicked[0], temp_clicked[1])

            temp_clicked = None
        else:
            print('click somewhere to set value')
        


#Open windows and detect clicks
cv2.namedWindow("Camera Feed")
cv2.namedWindow("Captured Image")
cv2.setMouseCallback("Camera Feed", raw_img_format)
cv2.setMouseCallback("Captured Image", main_click)

#Initialize Camera
image_feed = ImageAcquisition()

#Main image loop
while True:
    raw_img = image_feed.get_frame(raw_img)

    cv2.imshow('Camera Feed', raw_img)
    cv2.imshow("Captured Image", draw_buttons(color_img, temp_clicked, snspd, wvguide))

    if cv2.waitKey(1) & 0xFF == ord("q"):
        del image_feed
        cv2.closeAllWindows()
    
    if angle == None:
        angle = straighten_sequence(bw_img)
        raw_img = size_and_straighten(raw_img, angle or 0)
        bw_img = img_process_bw(color_img)
        print('angle set')
        print(angle)

