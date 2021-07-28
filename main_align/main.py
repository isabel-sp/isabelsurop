'''
Main file to run to align
'''

import img_process
import display_functions
import cv2
import time
import numpy as np

captured_img = None
color_img = np.zeros((1080,1440 ,3), np.uint8)
temp_clicked = None
snspd = None
wvguide = None

#update this with a live image feed
img_raw = cv2.imread('test_14401080.png')


#CALLBACK FUNCTIONS
def raw_img_format(event, x, y, flags, param):
    global captured_img
    global color_img

    if event == cv2.EVENT_LBUTTONDOWN:
        captured_img = cv2.cvtColor(img_raw,cv2.COLOR_BGR2GRAY)
        #captured_img = img_process.bw_green(captured_img)
        captured_img = cv2.resize(captured_img, (1440, 1080))

        color_img = cv2.resize(img_raw, (1440, 1080))

    
def main_click(event, x, y, flags, param):
    global captured_img
    global temp_clicked
    global snspd
    global wvguide

    if event == cv2.EVENT_LBUTTONDOWN:
        print('clicked')
        click = display_functions.button_clicked(x, y)
        if not click:
            print('marked point')
            #mark temporary point
            temp_clicked = (x, y)
        elif click == 'align' and snspd and wvguide:
            print('aligned')
            #RUN ALIGNMENT THING
            print('moving stage')
            time.sleep(2)
            stage_shift = 10 #in estimated pixels??
            print('stage moved x amount')

            #UPDATE CAPTURED IMAGE
            captured_img = cv2.cvtColor(img_raw,cv2.COLOR_BGR2GRAY)
            captured_img = cv2.resize(captured_img, (1440, 1080))

            #UPDATE VALUES
            temp_clicked = None
            #x_found_wvguide = img_process.temp_findline(captured_img[wvguide[1]], wvguide[0])
            x_found_wvguide = img_process.line_center_x(captured_img, x, y)[0]
            wvguide = (x_found_wvguide, wvguide[1])
            #search estimated area that snspd shifted to
            #x_found_snspd = img_process.temp_findline(captured_img[snspd[1]], snspd[0] + stage_shift) 
            x_found_snspd = img_process.line_center_x(captured_img, x + stage_shift, y)[0]
            snspd = (x_found_snspd, snspd[1])

        elif not temp_clicked == None:
            print('setting value')
            if click == 'snspd':
                #take temp and try to find snspd waveguide, set coordinate
                #x_found = img_process.temp_findline(captured_img[y], x)
                x_found = img_process.line_center_x(captured_img, temp_clicked[0], temp_clicked[1])[0]
                snspd = (x_found, y)
            elif click == 'wvguide':
                #take temp and try to find waveguide, set coordinate
                #x_found = img_process.temp_findline(captured_img[y], x)
                x_found = img_process.line_center_x(captured_img, temp_clicked[0], temp_clicked[1])[0]
                wvguide = (x_found, y)
            temp_clicked = None
        else:
            print('click somewhere to set value')
        


#Open windows and detect clicks
cv2.namedWindow("Camera Feed")
cv2.namedWindow("Captured Image")
cv2.setMouseCallback("Camera Feed", raw_img_format)
cv2.setMouseCallback("Captured Image", main_click)

while True:
    cv2.imshow("Camera Feed", img_raw)
    cv2.imshow("Captured Image", display_functions.draw_buttons(color_img, temp_clicked, snspd, wvguide))
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cv2.destroyAllWindows()


#CLOSE WINDOWS