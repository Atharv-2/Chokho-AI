from ultralytics import YOLO

model = YOLO('yolo11m.pt')

data_yaml = 'data/IntelligentVision-7/data.yaml'

results = model.train(data=data_yaml, epochs = 50, imgsz = 640, batch = 16, name = 'trash_model', patience = 10, save =True, plots = True)

