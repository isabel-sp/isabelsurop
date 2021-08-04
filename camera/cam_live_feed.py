try:
    # if on Windows, use the provided setup script to add the DLLs folder to the PATH
    from windows_setup import configure_path
    configure_path()
except ImportError:
    configure_path = None

from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, TLCamera, Frame
from thorlabs_tsi_sdk.tl_camera_enums import SENSOR_TYPE
from thorlabs_tsi_sdk.tl_mono_to_color_processor import MonoToColorProcessorSDK

try:
    #  For python 2.7 tkinter is named Tkinter
    import Tkinter as tk
except ImportError:
    import tkinter as tk
from PIL import Image, ImageTk
import typing
import threading
try:
    #  For Python 2.7 queue is named Queue
    import Queue as queue
except ImportError:
    import queue

import numpy as np
import cv2
import time

class ImageAcquisitionThread(threading.Thread):

    def __init__(self, camera):
        # type: (TLCamera) -> ImageAcquisitionThread
        super(ImageAcquisitionThread, self).__init__()
        self._camera = camera
        self._previous_timestamp = 0

        # setup color processing if necessary
        if self._camera.camera_sensor_type != SENSOR_TYPE.BAYER:
            # Sensor type is not compatible with the color processing library
            self._is_color = False
        else:
            self._mono_to_color_sdk = MonoToColorProcessorSDK()
            self._image_width = self._camera.image_width_pixels
            self._image_height = self._camera.image_height_pixels
            self._mono_to_color_processor = self._mono_to_color_sdk.create_mono_to_color_processor(
                SENSOR_TYPE.BAYER,
                self._camera.color_filter_array_phase,
                self._camera.get_color_correction_matrix(),
                self._camera.get_default_white_balance_matrix(),
                self._camera.bit_depth
            )
            self._is_color = True

        self._bit_depth = camera.bit_depth
        self._camera.image_poll_timeout_ms = 0  # Do not want to block for long periods of time
        self._image_queue = queue.Queue(maxsize=2)
        self._stop_event = threading.Event()

    def get_output_queue(self):
        return self._image_queue

    def stop(self):
        self._stop_event.set()

    def _get_color_image(self, frame):
        # type: (Frame) -> Image
        # verify the image size
        width = frame.image_buffer.shape[1]
        height = frame.image_buffer.shape[0]
        if (width != self._image_width) or (height != self._image_height):
            self._image_width = width
            self._image_height = height
            print("Image dimension change detected, image acquisition thread was updated")
        # color the image. transform_to_24 will scale to 8 bits per channel
        color_image_data = self._mono_to_color_processor.transform_to_24(frame.image_buffer,
                                                                         self._image_width,
                                                                         self._image_height)
        color_image_data = color_image_data.reshape(self._image_height, self._image_width, 3)
        # return PIL Image object
        return Image.fromarray(color_image_data, mode='RGB')

    def run_one_img(self):
        open_cv_image = None
        time.sleep(0.5)
        try:
            frame = self._camera.get_pending_frame_or_null()
            if not frame is None:
                pil_image = self._get_color_image(frame)
                open_cv_image = np.array(pil_image)
                open_cv_image = open_cv_image[:, :, ::-1].copy() 
                self._image_queue.put_nowait(pil_image)
        except queue.Full:
            pass
        except Exception as error:
                print("Encountered error: {error}, image acquisition will stop.".format(error=error))
        self._mono_to_color_processor.dispose()
        self._mono_to_color_sdk.dispose()
        return open_cv_image


if __name__ == "__main__":
    with TLCameraSDK() as sdk:
        camera_list = sdk.discover_available_cameras()
        with sdk.open_camera(camera_list[0]) as camera:

            cam_get = ImageAcquisitionThread(camera)
            # camera_widget = LiveViewCanvas(parent=root, image_queue=image_acquisition_thread.get_output_queue())

            print("Setting camera parameters...")
            camera.frames_per_trigger_zero_for_unlimited = 0
            camera.arm(2)
            camera.issue_software_trigger()

            print("Starting image acquisition thread...")
            cam_get.start()

            while True:
                frame = cam_get.run_one_img()
                if frame is not None:
                    print('showing frame')
                    cv2.imshow('frame', frame)

                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break

            print("Waiting for image acquisition thread to finish...")
            cam_get.stop()
            cam_get.join()

            print("Closing resources...")

    print("App terminated. Goodbye!")