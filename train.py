from ultralytics import YOLO
import torch


if __name__ == '__main__':
    torch.multiprocessing.set_start_method('spawn', force=True)
    
    model = YOLO('yolo11n.pt')
    
    data_yaml = 'data/merged_chokho_dataset/data.yaml'
    
    results = model.train(
        data=data_yaml,
        workers=0,
        epochs=100,
        imgsz=640,
        batch=16,
        name='trash_model_1',
        patience=20,
        device=0,
        plots=True,
        save=True,
        exist_ok=True
    )
    
    print(f"Training complete!")