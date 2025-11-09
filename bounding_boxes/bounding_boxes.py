import os

import cv2
from ultralytics import YOLO

from . import exceptions as e
from .models import DetectedObject


class BoundingBoxes():
    AGE_MODEL = 'age_net.caffemodel'
    AGE_PROTO = 'age_deploy.prototxt'
    GENDER_MODEL = 'gender_net.caffemodel'
    GENDER_PROTO = 'gender_deploy.prototxt'

    AGE_BUCKETS = [
        '(0-2)', '(4-6)', '(8-12)', '(15-20)',
        '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    GENDER_LIST = ['Male', 'Female']

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

    def __init__(
        self,
        model: str = 'yolo11n.pt',
        path_to_weights: str = '',
        filter: list[str] | None = None,
        enable_age_gender: bool = True,
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

        self._model = YOLO(os.path.join(path_to_weights, model))
        self.filter = filter
        self.enable_age_gender = enable_age_gender

        if self.enable_age_gender:
            try:
                self.age_net = cv2.dnn.readNet(
                    os.path.join(path_to_weights, self.AGE_MODEL),
                    os.path.join(path_to_weights, self.AGE_PROTO))
                self.gender_net = cv2.dnn.readNet(
                    os.path.join(path_to_weights, self.GENDER_MODEL),
                    os.path.join(path_to_weights, self.GENDER_PROTO))
            except Exception:
                raise FileNotFoundError(
                    'Модели для распознавания возраста/пола не найдены.')

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

    def _predict_age_gender(self, face_img):
        if face_img.size == 0:
            return None, None

        blob = cv2.dnn.blobFromImage(
            face_img, 1.0, (227, 227), self.MODEL_MEAN_VALUES, swapRB=False)

        self.gender_net.setInput(blob)
        gender_preds = self.gender_net.forward()
        gender = self.GENDER_LIST[gender_preds[0].argmax()]

        self.age_net.setInput(blob)
        age_preds = self.age_net.forward()
        age = self.AGE_BUCKETS[age_preds[0].argmax()]

        return gender, age

    def _detect_face(self, person_img):
        if person_img.size == 0:
            return None

        gray = cv2.cvtColor(person_img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            return None

        (fx, fy, fw, fh) = faces[0]
        face_roi = person_img[fy:fy+fh, fx:fx+fw]

        return face_roi

    def get_boxes(self, frame) -> list[DetectedObject]:
        results = self._model(frame, verbose=False)
        boxes = results[0].boxes

        detected_objects = []
        for box in boxes:
            class_name = self._model.names[int(box.cls)]

            if self._filter is not None and class_name not in self._filter:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            if class_name == 'person' and self.enable_age_gender:
                face = self._detect_face(frame[y1:y2, x1:x2])
                if face is not None:
                    gender, age = self._predict_age_gender(face)
                    if gender and age:
                        class_name = f'{gender}, Age: {age}'
                #     else:
                #         class_name = 'person (no face)'
                # else:
                #     class_name = 'person (no face)'

            detected_obj = DetectedObject(
                top_left=(x1, y1),
                bottom_right=(x2, y2),
                class_name=class_name,
                confidence=float(box.conf)
            )
            detected_objects.append(detected_obj)

        return detected_objects
