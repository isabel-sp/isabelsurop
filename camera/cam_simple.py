try:
    # if on Windows, use the provided setup script to add the DLLs folder to the PATH
    from windows_setup import configure_path
    configure_path()
except ImportError:
    configure_path = None

from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, TLCamera, Frame
from thorlabs_tsi_sdk.tl_camera_enums import SENSOR_TYPE
from thorlabs_tsi_sdk.tl_mono_to_color_processor import MonoToColorProcessorSDK


from PIL import Image
import typing
import threading
import queue
import numpy as np
import cv2


with TLCameraSDK() as camera_sdk, MonoToColorProcessorSDK() as mono_to_color_sdk:
    available_cameras = camera_sdk.discover_available_cameras()
    if len(available_cameras) < 1:
        raise ValueError("no cameras detected")

    with camera_sdk.open_camera(available_cameras[0]) as camera:
        camera.frames_per_trigger_zero_for_unlimited = 0 
        camera.image_poll_timeout_ms = 2000
        camera.arm(2)

        image_width = camera.image_width_pixels
        image_height = camera.image_height_pixels
        camera.issue_software_trigger()
        frame = camera.get_pending_frame_or_null()
        
        if frame is not None: print("frame received!")
        else: raise ValueError("No frame arrived within the timeout!")

        camera.disarm()

        with mono_to_color_sdk.create_mono_to_color_processor(
            camera.camera_sensor_type,
            camera.color_filter_array_phase,
            camera.get_color_correction_matrix(),
            camera.get_default_white_balance_matrix(),
            camera.bit_depth
        ) as mono_to_color_processor:

            #mono_to_color_processor.color_space = COLOR_SPACE.SRGB  # sRGB color space
            #mono_to_color_processor.output_format = FORMAT.RGB_PIXEL  # data is returned as sequential RGB values

            print("Red Gain = {red_gain}\nGreen Gain = {green_gain}\nBlue Gain = {blue_gain}\n".format(
                red_gain=mono_to_color_processor.red_gain,
                green_gain=mono_to_color_processor.green_gain,
                blue_gain=mono_to_color_processor.blue_gain
            ))

            color_image_data = mono_to_color_processor.transform_to_24(frame.image_buffer, image_width, image_height)
            color_image_data = color_image_data.reshape(image_height, image_width, 3)
            pil_image = Image.fromarray(color_image_data, mode = 'RGB') 
            open_cv_image = np.array(pil_image)
            open_cv_image = open_cv_image[:, :, ::-1].copy() 
            
            #display image
            cv2.imwrite('opencv_image.png', open_cv_image)
            cv2.imshow('image', open_cv_image)
            cv2.waitKey(0)
            cv2.closeAllWindows()


print("program completed")