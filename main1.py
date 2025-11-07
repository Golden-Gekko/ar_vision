import cv2
from ultralytics import YOLO

# for i in range(4):
#     cap = cv2.VideoCapture(i)
#     if cap.isOpened():
#         print(f'Камера {i} доступна')
#         cap.release()
#     else:
#         print(f'Камера {i} не найдена')

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Устанавливаем ширину
cap.set(4, 480)  # Устанавливаем высоту

model = YOLO('yolo-Weights/yolov8n.pt')

while True:
    ret, frame = cap.read()
    if not ret:
        s = '*** Не удалось захватить кадр ***'
        print('*' * len(s), s, '*' * len(s), sep='\n')
        break

    results = model(frame)[0]
    
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf)
            cls = int(box.cls)
            name = model.names[cls]
            
            label = f"{name} {conf:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
    
    cv2.imshow('YOLO Detection', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
