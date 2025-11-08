import json
import os

import cv2
import numpy as np

from bounding_boxes import BoundingBoxes, DetectedObject
from camera_tool import CameraTool
from window import Window


class DetectionApp:
    BOX_THICKNESS = 2
    TEXT_OFFSET = 10
    TEXT_THICKNESS = 2
    TEXT_FONTSCALE = 0.6

    def __init__(
        self,
        camera: CameraTool,
        detector: BoundingBoxes,
        box_colors: dict[str, tuple[int, int, int]] | None = None,

    ):
        self.camera = camera
        self.detector = detector
        self.box_colors = box_colors
        self.show_camera = True

    def get_frame_with_detections(self):
        try:
            frame = self.camera.read()
            detections = self.detector.get_boxes(frame)
            if not self.show_camera:
                h, w = frame.shape[:2]
                frame = np.zeros((h, w, 4), dtype=np.uint8)
            self._draw_detections(frame, detections)
            return frame
        except Exception as e:
            print(f'Ошибка при получении кадра: {e}')
            return None

    @staticmethod
    def _draw_detections(frame, detections: list[DetectedObject]):
        for obj in detections:
            cv2.rectangle(
                frame, obj.top_left, obj.bottom_right,
                (255, 0, 255),
                DetectionApp.BOX_THICKNESS)

            pos = obj.top_left[1] - DetectionApp.TEXT_OFFSET
            cv2.putText(
                frame,
                f'{obj.class_name} {obj.confidence:.2f}',
                (obj.top_left[0], max(pos, DetectionApp.TEXT_OFFSET)),
                cv2.FONT_HERSHEY_SIMPLEX,
                DetectionApp.TEXT_FONTSCALE,
                (255, 0, 255),
                DetectionApp.TEXT_THICKNESS
            )

    def increment_camera_scale(self):
        self.camera.scale = self.camera.scale + 1

    def decrement_camera_scale(self):
        self.camera.scale = self.camera.scale - 1

    def toggle_camera_showing(self):
        self.show_camera = not self.show_camera


def load_config(config_path: str) -> dict:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f'Файл конфигурации не найден: {config_path}')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    try:
        with (
            CameraTool(**config['camera']) as camera,
            Window(**config['window']) as window
        ):
            detector = BoundingBoxes(**config['detection'])
            app = DetectionApp(camera, detector)

            window.set_key_callback('+', app.increment_camera_scale)
            window.set_key_callback('-', app.decrement_camera_scale)
            window.set_key_callback('t', app.toggle_camera_showing)
            width, height = window.run(
                data_source=app.get_frame_with_detections)
            scale = camera.scale

    except Exception as e:
        print(f'Ошибка: {e}')


if __name__ == "__main__":
    main()
    # from tools import check_available_monitors
    # check_available_monitors()
