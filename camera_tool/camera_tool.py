from typing import Optional

import cv2

from .import exceptions as e


class CameraTool:
    def __init__(self, camera_number: int = 0):
        self._camera: Optional[cv2.VideoCapture] = None
        self.connect(camera_number)
        self._scale = 1

    def _scale_frame(self, frame):
        return frame

    def read(self):
        if self._camera is None:
            raise e.CameraClosedError()

        isOk, frame = self._camera.read()

        if not isOk:
            raise e.FrameReadError()

        return self._scale_frame(frame)

    def connect(self, camera_number: int = 0):
        self.release()
        self._camera = cv2.VideoCapture(camera_number)
        if not self._camera.isOpened():
            raise e.CameraError(camera_number=camera_number)

    def release(self):
        if self._camera is not None:
            self._camera.release()
            self._camera = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
