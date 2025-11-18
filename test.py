from ultralytics import YOLO

model = YOLO("runs/detect/trash_model/weights/best.pt")

model.predict(source= "1.webp",show = True , save = True)
