#Camera class

from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, TLCamera, Frame
from thorlabs_tsi_sdk.tl_camera_enums import SENSOR_TYPE
from thorlabs_tsi_sdk.tl_mono_to_color_processor import MonoToColorProcessorSDK
import cv2
import numpy as np
from PIL import Image

class ImageAcquisition():

    def __init__(self, camera):
        self.camera = camera
        self._mono_to_color_sdk = MonoToColorProcessorSDK()
        self._image_width = self.camera.image_width_pixels
        self._image_height = self.camera.image_height_pixels
        self._mono_to_color_processor = self._mono_to_color_sdk.create_mono_to_color_processor(
            SENSOR_TYPE.BAYER,
            self.camera.color_filter_array_phase,
            self.camera.get_color_correction_matrix(),
            self.camera.get_default_white_balance_matrix(),
            self.camera.bit_depth
        )
        camera.frames_per_trigger_zero_for_unlimited = 0
        camera.arm(2)
        camera.issue_software_trigger()

    def get_frame(self, raw_img):
        frame = self.camera.get_pending_frame_or_null()
        if frame is not None:
            width = frame.image_buffer.shape[1]
            height = frame.image_buffer.shape[0]
            color_image_data = self._mono_to_color_processor.transform_to_24(frame.image_buffer, width, height)
            color_image_data = color_image_data.reshape(height, width, 3)
            pil_image = Image.fromarray(color_image_data, mode = 'RGB')
            raw_img = np.array(pil_image)
            raw_img = raw_img[:, :, ::-1].copy()
        return raw_img
    
    def __del__(self):
        self._mono_to_color_processor.dispose()
        self._mono_to_color_sdk.dispose()
