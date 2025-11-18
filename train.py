from ultralytics import YOLO
import torch


if __name__ == '__main__':
    # Set multiprocessing start method for Windows
    torch.multiprocessing.set_start_method('spawn', force=True)
    
    model = YOLO('yolo11m.pt')

    data_yaml = 'data/merged_chokho_dataset'

    results = model.train(data=data_yaml, workers=0, epochs=100, imgsz=640, batch=16, name='trash_model', patience=20, augment=True, mosaic=1.0, mixup=0.15, degrees=10, flipud=0.5, fliplr=0.5, save=True, device=0, plots=True)

print(f"Best mAP50: {results.results_dict['metrics/mAP50(B)']:.3f}")