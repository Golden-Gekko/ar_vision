class CameraError(Exception):
    def __init__(self, camera_number: int | None = None):
        super().__init__('Не удалось подключиться к камере' + (
            f' с номером {camera_number}.' if camera_number else '.'))


class FrameReadError(Exception):
    def __init__(self):
        super().__init__('Ошибка захвата кадра.')


class CameraClosedError(Exception):
    def __init__(self):
        super().__init__('Попытка чтения из закрытой камеры.')


class ResolutionNotSupportedError(Exception):
    def __init__(self, width: int, height: int):
        super().__init__(f'Разрешение {width} x {height} не поддерживается.')


class FPSNotSupportedError(Exception):
    def __init__(self, fps: int):
        super().__init__(f'Частота кадров {fps} не поддерживается.')
