class BoundingBoxesInitError(Exception):
    def __init__(self):
        super().__init__(
            'Параметры конструктора класса BoundingBoxes должны '
            'быть типа "str"')


class FilterSetterError(Exception):
    def __init__(self, is_item_error: bool = False):
        if is_item_error:
            super().__init__('Все элементы filter должны быть строками.')
        else:
            super().__init__('filter должен быть списком строк.')
