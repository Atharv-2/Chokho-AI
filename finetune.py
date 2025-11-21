from ultralytics import YOLO
import torch


if __name__ == '__main__':
    # Set multiprocessing start method for Windows
    torch.multiprocessing.set_start_method('spawn', force=True)
    
    model = YOLO('best.pt')
    
    data_yaml = 'data/merged_chokho_dataset/data.yaml'
    
    results = model.train(
        data=data_yaml,
        epochs=30,                    # Conservative for fine-tuning
        imgsz=640,
        batch=16,
        workers=0,
        device=0,                     # GPU device
        patience=10,                  # Early stopping
        lr0=0.0005,                   # 50x lower learning rate (transfer learning)
        lrf=0.0005,                   # Final learning rate
        name='trash_model_finetuned', # Save as new experiment
        augment=True,
        mosaic=1.0,
        mixup=0.20,                   # Increased for weak classes
        degrees=15,                   # More augmentation
        flipud=0.5,
        fliplr=0.5,
        erasing=0.4,                  # Random erasing for robustness
        save=True,
        plots=True,
        verbose=True,
        weight_decay=0.0005,          # Regularization
        warmup_epochs=3,              # Gradual warmup
        resume=False,
        pretrained=True,
    )
    