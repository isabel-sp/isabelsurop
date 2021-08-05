try:
    # if on Windows, use the provided setup script to add the DLLs folder to the PATH
    from windows_setup import configure_path
    configure_path()
except ImportError:
    configure_path = None

from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, TLCamera, Frame
from thorlabs_tsi_sdk.tl_camera_enums import SENSOR_TYPE
from thorlabs_tsi_sdk.tl_mono_to_color_processor import MonoToColorProcessorSDK

import tkinter as tk
from PIL import Image, ImageTk
import typing
import threading
import queue
import cv2
import numpy as np


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

        open_cv_image = np.zeros((1080,1440 ,3), np.uint8)

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
                open_cv_image = np.array(pil_image)
                open_cv_image = open_cv_image[:, :, ::-1].copy()


            cv2.imshow('Live Camera Feed', open_cv_image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                mono_to_color_processor.dispose()
                mono_to_color_sdk.dispose()
                cv2.closeAllWindows()
        
        
        



                
                    


