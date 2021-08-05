'''
Main file to run to align
'''

from windows_setup import configure_path
configure_path()

from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, TLCamera, Frame
from thorlabs_tsi_sdk.tl_camera_enums import SENSOR_TYPE
from thorlabs_tsi_sdk.tl_mono_to_color_processor import MonoToColorProcessorSDK

import cv2
from PIL import Image, ImageTk
import time
import numpy as np
from cam_helper import *
from display_functions import *
from img_process import *
from piezo_helper import *
from straighten import straighten_sequence

raw_img = None
bw_img = None
color_img = np.zeros((1080,1440 ,3), np.uint8)
temp_clicked = None
snspd = None
wvguide = None
angle = 0
pzt = PZT_driver()


#CALLBACK FUNCTIONS
def raw_img_format(event, x, y, flags, param):
    global bw_img
    global color_img
    global angle

    if event == cv2.EVENT_LBUTTONDOWN:
        color_img = size_and_straighten(raw_img, angle or 0)
        bw_img = img_process_bw(color_img)

        cv2.imwrite('bw_img.png', bw_img)

    
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
                x_found = find_light_point(bw_img, temp_clicked[0], temp_clicked[1])
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


with TLCameraSDK() as sdk:
    camera_list = sdk.discover_available_cameras()
    with sdk.open_camera(camera_list[0]) as camera:
        mono_to_color_sdk = MonoToColorProcessorSDK()
        mono_to_color_processor = mono_to_color_sdk.create_mono_to_color_processor(
            SENSOR_TYPE.BAYER,
            camera.color_filter_array_phase,
            camera.get_color_correction_matrix(),
            camera.get_default_white_balance_matrix(),
            camera.bit_depth
        )
        camera.frames_per_trigger_zero_for_unlimited = 0
        camera.arm(2)
        camera.issue_software_trigger()

        raw_img = np.zeros((1080,1440 ,3), np.uint8)

        while True:

            frame = camera.get_pending_frame_or_null()
            print(frame)
            if frame is not None:
                width = frame.image_buffer.shape[1]
                height = frame.image_buffer.shape[0]
                color_image_data = mono_to_color_processor.transform_to_24(frame.image_buffer, width, height)
                print(color_image_data)
                color_image_data = color_image_data.reshape(height, width, 3)
                pil_image = Image.fromarray(color_image_data, mode = 'RGB')
                raw_img = np.array(pil_image)
                raw_img = raw_img[:, :, ::-1].copy()


            cv2.imshow('Camera Feed', raw_img)
            cv2.imshow("Captured Image", draw_buttons(color_img, temp_clicked, snspd, wvguide))

            if cv2.waitKey(1) & 0xFF == ord("q"):
                mono_to_color_processor.dispose()
                mono_to_color_sdk.dispose()
                cv2.closeAllWindows()
            
            if angle == None:
                angle = straighten_sequence(bw_img)
                raw_img = size_and_straighten(raw_img, angle or 0)
                bw_img = img_process_bw(color_img)
                print('angle set')
                print(angle)

