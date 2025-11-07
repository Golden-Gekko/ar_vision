import os

from ultralytics import YOLO

from . import exceptions as e
from models import DetectedObject


class BoundingBoxes():
    def __init__(
        self,
        model: str = 'yolo11n.pt',
        path_to_weights: str = '',
        filter: list[str] | None = None,
    ):
        for name, value in [
            ('model', model), ('path_to_weights', path_to_weights)
        ]:
            if not isinstance(value, str):
                raise TypeError(
                    f'{name} должен быть типа "str", '
                    f'имеется {type(value).__name__}')

        if not isinstance(model, str) or not isinstance(path_to_weights, str):
            raise e.BoundingBoxesInitError()
        if not os.path.isdir(path_to_weights):
            raise e.WeightsPathError(path_to_weights)

        self._model = YOLO(os.path.join(path_to_weights, model))
        self.filter = filter

    def get_classes_list(self) -> list[str]:
        return list(self._model.names.values())

    @property
    def filter(self) -> list[str] | None:
        return self._filter

    @filter.setter
    def filter(self, value: list[str] | None) -> None:
        if value is None:
            self._filter = None
            return
        if not isinstance(value, list):
            raise e.FilterSetterError()
        if not all(isinstance(item, str) for item in value):
            raise e.FilterSetterError(True)
        self._filter = value

    def get_boxes(self, frame) -> list[DetectedObject]:
        results = self._model(frame)
        boxes = results[0].boxes

        detected_objects = []
        for box in boxes:
            class_name = self._model.names[int(box.cls)]

            if self._filter is not None and class_name not in self._filter:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            detected_obj = DetectedObject(
                top_left=(x1, y1),
                bottom_right=(x2, y2),
                class_name=class_name,
                confidence=float(box.conf)
            )
            detected_objects.append(detected_obj)

        return detected_objects
