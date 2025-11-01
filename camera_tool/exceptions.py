class CameraError(Exception):
    def __init__(self, camera_number: int | None = None):
        super().__init__('Не удалось открыть камеру' + (
            f' с номером {camera_number}.' if camera_number else '.'))


class FrameReadError(Exception):
    def __init__(self):
        super().__init__('Ошибка захвата кадра.')


class CameraClosedError(Exception):
    def __init__(self):
        super().__init__('Попытка чтения из закрытой камеры.')
