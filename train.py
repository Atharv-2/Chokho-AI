from ultralytics import YOLO
import torch


if __name__ == '__main__':
    # Set multiprocessing start method for Windows
    torch.multiprocessing.set_start_method('spawn', force=True)
    
    model = YOLO('yolo11m.pt')

    data_yaml = 'data/IntelligentVision-7/data.yaml'

    results = model.train(data=data_yaml, workers=0, epochs=50, imgsz=640, batch=8, name='trash_model', patience=10, save=True, device=0, plots=True)

