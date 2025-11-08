import argparse
import json
import os

import cv2
import numpy as np

from bounding_boxes import BoundingBoxes, DetectedObject
from camera_tool import CameraTool
from window import Window


def load_config(config_path: str) -> dict:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f'Файл конфигурации не найден: {config_path}')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_config(config_path: str, config: dict):
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def parse_args():
    parser = argparse.ArgumentParser(
        description='YOLO Object Detection Application'
    )
    parser.add_argument(
        '--all-cameras',
        action='store_true',
        help='Проверить все доступные камеры'
    )
    parser.add_argument(
        '--all-monitors',
        action='store_true',
        help='Проверить все мониторы'
    )
    parser.add_argument(
        '--camera', type=int,
        help='Номер камеры (переопределяет config)'
    )
    parser.add_argument(
        '--monitor', type=int,
        help='Номер монитора (переопределяет config)'
    )
    parser.add_argument(
        '--full-screen',
        action='store_true',
        help='Запустить окно в полноэкранном режиме'
    )
    parser.add_argument(
        '--model',
        type=str,
        help='Имя модели (переопределяет config)'
    )
    parser.add_argument(
        '--reset',
        action='store_true',
        help='Сбросить config.json к настройкам по умолчанию'
    )
    return parser.parse_args()


def apply_cli_args(config: dict, args) -> dict:
    if args.camera is not None:
        config['camera']['camera_number'] = args.camera

    if args.monitor is not None:
        config['window']['monitor_number'] = args.monitor

    if args.full_screen:
        config['window']['width'] = None
        config['window']['height'] = None

    if args.model is not None:
        config['detection']['model'] = args.model

    return config


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


def main(args):
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    config = apply_cli_args(load_config(config_path), args)

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
        return

    config['camera']['scale'] = scale
    config['window']['width'] = width
    config['window']['height'] = height

    try:
        save_config(config_path, config)
        print('Настройки сохранены')
    except Exception as e:
        print(f'Не удалось сохранить config.json: {e}')


if __name__ == '__main__':
    args = parse_args()

    if args.reset:
        from default_config import DEFAULT_CONFIG
        try:
            save_config(
                os.path.join(os.path.dirname(__file__), 'config.json'),
                DEFAULT_CONFIG)
            print('config.json успешно сброшен.')
        except Exception as e:
            print(f'Ошибка при сбросе: {e}')
    elif args.all_cameras:
        from tools import check_available_cameras
        check_available_cameras()
    elif args.all_monitors:
        from tools import check_available_monitors
        check_available_monitors()
    else:
        main(args)
