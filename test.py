from ultralytics import YOLO

model = YOLO("best.pt")

model.predict(source= "44.jpg",show = True , save = True)
