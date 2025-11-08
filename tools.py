import cv2
import numpy as np

from camera_tool import CameraTool
from window import Window


def check_available_cameras():
    camera_list = CameraTool.list_available_cameras()
    for camera_number in camera_list:
        with (
            CameraTool(camera_number=camera_number) as camera,
            Window(width=640, height=480) as window
        ):
            def get_frame():
                frame = camera.read()
                cv2.putText(
                    frame, f'Camera N{camera_number}',
                    (10, frame.shape[0] // 2), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 2)
                return frame

            window.run(data_source=get_frame)


def check_available_monitors():
    for monitor_number in range(len(Window.get_monitors_info())):
        with Window(
            monitor_number=monitor_number, width=640, height=480
        ) as window:
            def get_frame():
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(
                    frame, f'Monitor N{monitor_number}',
                    (10, 240), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 2)
                return frame
            window.run(data_source=get_frame)
