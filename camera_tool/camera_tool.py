from typing import Optional

import cv2

from .import exceptions as e


class CameraTool:
    def __init__(
        self,
        camera_number: int = 0,
        width: int = 640,
        height: int = 480,
        fps: int = 30,
    ):
        for name, value in [
            ('camera_number', camera_number),
            ('width', width),
            ('height', height),
            ('fps', fps)
        ]:
            if not isinstance(value, int):
                raise TypeError(
                    f'{name} должен быть типа "int", '
                    f'имеется {type(value).__name__}')

        self._camera: Optional[cv2.VideoCapture] = None
        self.connect(camera_number)
        self.set_resolution(width, height)
        self.set_fps(fps)
        self._scale = 1

    @staticmethod
    def list_available_cameras(
        max_number_cameras: int = 1,
    ) -> list[int] | None:
        camera_list = []
        cur_lvl = cv2.getLogLevel()
        cv2.setLogLevel(0)
        for i in range(max_number_cameras):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                camera_list.append(i)
        cv2.setLogLevel(cur_lvl)
        return camera_list if camera_list else None

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

    def set_resolution(self, width: int = 640, height: int = 480):
        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        if (width, height) != self.get_resolution():
            raise e.ResolutionNotSupportedError(width, height)

    def get_resolution(self) -> tuple[int, int]:
        actual_width = int(self._camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self._camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return actual_width, actual_height

    def set_fps(self, fps: int = 30):
        self._camera.set(cv2.CAP_PROP_FPS, fps)
        if fps != self.get_fps():
            raise e.FPSNotSupportedError(fps)

    def get_fps(self) -> int:
        return int(self._camera.get(cv2.CAP_PROP_FPS))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
