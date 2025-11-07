import os


class BoundingBoxesInitError(Exception):
    def __init__(self):
        super().__init__(
            'Параметры конструктора класса BoundingBoxes должны '
            'быть типа "str"')


class WeightsPathError(Exception):
    def __init__(self, path: str):
        super().__init__(
            f'Указанная директория существует: {os.path.abspath(path)}.')


class FilterSetterError(Exception):
    def __init__(self, is_item_error: bool = False):
        if is_item_error:
            super().__init__('Все элементы filter должны быть строками.')
        else:
            super().__init__('filter должен быть списком строк.')
