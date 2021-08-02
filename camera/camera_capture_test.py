import numpy as np
import sys
from PIL import Image
import os
import cv2 as cv2
import matplotlib.pyplot as plt

#PATH THINGS
print("original environment path")
print(os.environ['PATH'])

try:
    from windows_setup import configure_path
    configure_path()
except ImportError:
    configure_path = None

print("New Environment Path")
print(os.environ['PATH'])

from thorlabs_tsi_sdk.tl_camera import TLCameraSDK
from thorlabs_tsi_sdk.tl_mono_to_color_processor import MonoToColorProcessorSDK
from thorlabs_tsi_sdk.tl_mono_to_color_enums import COLOR_SPACE
from thorlabs_tsi_sdk.tl_color_enums import FORMAT

with TLCameraSDK() as camera_sdk, MonoToColorProcessorSDK() as mono_to_color_sdk:
    available_cameras = camera_sdk.discover_available_cameras()
    if len(available_cameras) < 1:
        raise ValueError("no cameras detected")

    with camera_sdk.open_camera(available_cameras[0]) as camera:
        camera.frames_per_trigger_zero_for_unlimited = 0  # start camera in continuous mode
        camera.image_poll_timeout_ms = 2000  # 2 second timeout
        camera.arm(2)

        image_width = camera.image_width_pixels
        image_height = camera.image_height_pixels

        camera.issue_software_trigger()

        frame = camera.get_pending_frame_or_null()
        if frame is not None:
            print("frame received!")
        else:
            raise ValueError("No frame arrived within the timeout!")

        camera.disarm()

        """
            When creating a mono to color processor, we want to initialize it using parameters from the camera.
        """
        with mono_to_color_sdk.create_mono_to_color_processor(
            camera.camera_sensor_type,
            camera.color_filter_array_phase,
            camera.get_color_correction_matrix(),
            camera.get_default_white_balance_matrix(),
            camera.bit_depth
        ) as mono_to_color_processor:

            mono_to_color_processor.color_space = COLOR_SPACE.SRGB  # sRGB color space
            mono_to_color_processor.output_format = FORMAT.BGR_PIXEL  # data is returned as sequential RGB values

            print("Red Gain = {red_gain}\nGreen Gain = {green_gain}\nBlue Gain = {blue_gain}\n".format(
                red_gain=mono_to_color_processor.red_gain,
                green_gain=mono_to_color_processor.green_gain,
                blue_gain=mono_to_color_processor.blue_gain
            ))

            # this will give us a resulting image with 3 channels (RGB) and 16 bits per channel, resulting in 48 bpp
            color_image_48_bpp = mono_to_color_processor.transform_to_48(frame.image_buffer, image_width, image_height)

            # try to format and display
            #currently 1555200 numbersz
            #need to format to numpy array of dimentions (1080, 1440, 3)


            print(color_image_48_bpp)
            print(color_image_48_bpp.shape)

            new_img = []
            for y in range(1080):
                row = []
                for x in range(1440):
                    pixel = []
                    for p in range(3):
                        pixel.append(color_image_48_bpp[p + 3*x + 3*1440*y])
                    row.append(pixel)
                new_img.append(row)
            new_img = np.array(new_img)
            print(np.shape(new_img))
            cv2.imwrite('somethingnew.png', new_img)
            cv2.imshow('image', new_img)
            cv2.waitKey(0)
            cv2.closeAllWindows()

            plt.plot(color_image_48_bpp)
            plt.show()

            img = np.reshape(color_image_48_bpp, (1440, 1080, 3))
            print(img)

            #display image
            cv2.imwrite('something.png', img)

            cv2.imshow('image', img)
            
            cv2.waitKey(0)
            cv2.closeAllWindows()


#  Because we are using the 'with' statement context-manager, disposal has been taken care of.

print("program completed")
