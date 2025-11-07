import cv2
import win32api

from .import exceptions as e


class Window():
    def __init__(
        self,
        monitor_number: int = 0,
        width: int | None = None,
        height: int | None = None,
        window_name: str = 'Default',
    ):
        for name, value in [
            ('monitor_number', monitor_number),
            ('width', width),
            ('height', height)
        ]:
            if not isinstance(value, int):
                raise TypeError(
                    f'{name} должен быть типа "int", '
                    f'имеется {type(value).__name__}')

        if not isinstance(window_name, str):
            raise TypeError(
                'window_name должен быть типа "str", имеется '
                f'{type(value).__name__}')

        monitors_info = Window.get_monitors_info()
        self.window_name = window_name
        if monitor_number > len(monitors_info):
            raise e.MonitorNumberError(monitor_number)

        x, y, w, h = monitors_info[monitor_number]
        w = min(w - x, width) if width is not None else (w - x)
        h = min(h - y, height) if height is not None else (h - y)

        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(window_name, x, y)
        cv2.resizeWindow(window_name, w, h)

        self.key_callbacks = {}

    @staticmethod
    def get_monitors_info() -> list[tuple[int]]:
        monitors = win32api.EnumDisplayMonitors()
        return [win32api.GetMonitorInfo(m[0])['Monitor'] for m in monitors]

    def set_key_callback(self, key, callback):
        if isinstance(key, str) and len(key) == 1:
            key = ord(key.lower())
        self.key_callbacks[key] = callback

    def update(self, frame):
        cv2.imshow(self.window_name, frame)

    def run(self, data_source=None):
        while True:
            if data_source is not None:
                frame = data_source()
                if frame is not None:
                    self.update(frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break

            if key in self.key_callbacks:
                callback = self.key_callbacks[key]
                try:
                    callback()
                except Exception as e:
                    print(f'Ошибка в callback для клавиши {chr(key)}: {e}')

        cv2.destroyAllWindows()
