import cv2
from ultralytics import YOLO
import win32api

# for i in range(4):
#    cap = cv2.VideoCapture(i)
#    if cap.isOpened():
#        print(f'Камера {i} доступна')
#        cap.release()
#    else:
#        print(f'Камера {i} не найдена')

cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("Ошибка: не удалось открыть камеру.")
# else:
#     # Словарь параметров для удобного отображения
#     props = {
#         'CV_CAP_PROP_FRAME_WIDTH': cv2.CAP_PROP_FRAME_WIDTH,
#         'CV_CAP_PROP_FRAME_HEIGHT': cv2.CAP_PROP_FRAME_HEIGHT,
#         'CV_CAP_PROP_FPS': cv2.CAP_PROP_FPS,
#         'CV_CAP_PROP_BRIGHTNESS': cv2.CAP_PROP_BRIGHTNESS,
#         'CV_CAP_PROP_CONTRAST': cv2.CAP_PROP_CONTRAST,
#         'CV_CAP_PROP_SATURATION': cv2.CAP_PROP_SATURATION,
#         'CV_CAP_PROP_GAIN': cv2.CAP_PROP_GAIN,
#         'CV_CAP_PROP_EXPOSURE': cv2.CAP_PROP_EXPOSURE,
#         'CV_CAP_PROP_FOURCC': cv2.CAP_PROP_FOURCC,
#         'CV_CAP_PROP_AUTOFOCUS': cv2.CAP_PROP_AUTOFOCUS,
#         'CV_CAP_PROP_FOCUS': cv2.CAP_PROP_FOCUS,
#     }

#     for name, prop_id in props.items():
#         value = cap.get(prop_id)
#         print(f"{name}: {value}")

# width = 1280
# height = 720

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Проверим, какое разрешение реально установлено
# actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# print(f"Запрошенное разрешение: {width}x{height}")
# print(f"Фактическое разрешение: {int(actual_width)}x{int(actual_height)}")
# cap.release()

monitors = win32api.EnumDisplayMonitors()
if len(monitors) > 1:
    monitor_info = monitors[1]
    x_offset = monitor_info[2][0]  # X левого верхнего угла
    y_offset = monitor_info[2][1]  # Y левого верхнего угла
    width = monitor_info[2][2] - x_offset  # Ширина
    height = monitor_info[2][3] - y_offset  # Высота
else:
    # Если второго монитора нет — используем основной
    x_offset, y_offset, width, height = 0, 0, 1920, 1080

# Создаём окно и перемещаем на второй монитор
cv2.namedWindow('AR View', cv2.WINDOW_NORMAL)
cv2.resizeWindow('AR View', width, height)
cv2.moveWindow('AR View', x_offset, y_offset)

model = YOLO('yolo11n.pt')

while True:
    ret, frame = cap.read()

    if not ret:
        s = '*** Не удалось захватить кадр ***'
        print('*' * len(s), s, '*' * len(s), sep='\n')
        break
    results = model(frame)
    
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf)
            cls = int(box.cls)
            name = model.names[cls]
            
            label = f"{name} {conf:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 1)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 1)
    
    cv2.imshow('AR View', frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
