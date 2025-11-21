"""
Advanced Fine-tuning: Multi-dataset training with class weighting
Focus on plastic and weak classes across all datasets
"""

from ultralytics import YOLO
import torch
import yaml
import os
from pathlib import Path

if __name__ == '__main__':
    torch.multiprocessing.set_start_method('spawn', force=True)
    
    print("\n" + "=" * 80)
    print("ADVANCED FINE-TUNING: Multi-Dataset with Class Focus")
    print("=" * 80)
    
    # Available datasets
    datasets = [
        ('data/GARBAGE-CLASSIFICATION-3-2/data.yaml', 'GARBAGE-CLASSIFICATION (6 classes)'),
        ('data/Domestic-Trash--1/data.yaml', 'Domestic-Trash (3 classes)'),
        ('data/garbage_best-1/data.yaml', 'Garbage-Best (6 classes)'),
    ]
    
    print("\n📊 Available datasets:")
    for path, name in datasets:
        if os.path.exists(path):
            with open(path) as f:
                config = yaml.safe_load(f)
                print(f"   ✅ {name}")
                print(f"      Classes: {config['names']}")
        else:
            print(f"   ❌ {name} - NOT FOUND")
    
    # Strategy: Start with GARBAGE dataset (has explicit PLASTIC class)
    primary_dataset = 'data/GARBAGE-CLASSIFICATION-3-2/data.yaml'
    
    print(f"\n🎯 PRIMARY DATASET: GARBAGE-CLASSIFICATION (PLASTIC focus)")
    print(f"\n💡 Fine-tuning Strategy:")
    print("   1. Load best.pt (85% mAP50 on merged dataset)")
    print("   2. Train on GARBAGE dataset (explicit PLASTIC class)")
    print("   3. Lower learning rate (transfer learning)")
    print("   4. More augmentation for robustness")
    print("   5. Early stopping if no improvement")
    
    print("\n🔄 Loading pre-trained model...")
    model = YOLO('runs/detect/trash_model/weights/best.pt')
    
    print(f"\n🚀 Starting fine-tuning with GARBAGE-CLASSIFICATION dataset...\n")
    
    # Fine-tune specifically on plastic/underperforming classes
    results = model.train(
        data=primary_dataset,
        epochs=25,                     # Conservative fine-tuning
        imgsz=640,
        batch=16,
        workers=0,
        device=0,
        patience=8,                    # Stop if no improvement for 8 epochs
        lr0=0.0005,                    # Very low learning rate (50x lower)
        lrf=0.0005,
        name='trash_plastic_finetuned',
        augment=True,
        mosaic=1.0,
        mixup=0.20,                    # Increased mixup for weak class learning
        degrees=15,                    # More rotation augmentation
        flipud=0.5,
        fliplr=0.5,
        erasing=0.4,                   # Random erasing augmentation
        save=True,
        plots=True,
        verbose=True,
        # Regularization for small dataset
        weight_decay=0.0005,
        warmup_epochs=3,
        warmup_momentum=0.8,
    )
    
    print("\n" + "=" * 80)
    print("✅ PHASE 1 COMPLETE: GARBAGE Dataset Fine-tuning")
    print("=" * 80)
    
    # Optional: Second phase on Domestic-Trash
    print("\n\n" + "=" * 80)
    print("PHASE 2: Fine-tuning on DOMESTIC-TRASH Dataset")
    print("=" * 80)
    print("\nThis will further improve on household waste categories...")
    
    response = input("\nContinue with Phase 2? (y/n): ").lower()
    
    if response == 'y':
        print("\n🔄 Loading fine-tuned model from Phase 1...")
        model = YOLO('runs/detect/trash_plastic_finetuned/weights/best.pt')
        
        print("\n🚀 Starting Phase 2 fine-tuning...\n")
        
        results = model.train(
            data='data/Domestic-Trash--1/data.yaml',
            epochs=20,
            imgsz=640,
            batch=16,
            workers=0,
            device=0,
            patience=6,
            lr0=0.0003,                # Even lower learning rate
            lrf=0.0003,
            name='trash_domestic_finetuned',
            augment=True,
            mosaic=1.0,
            mixup=0.20,
            degrees=15,
            flipud=0.5,
            fliplr=0.5,
            erasing=0.4,
            save=True,
            plots=True,
            verbose=True,
            weight_decay=0.0005,
            warmup_epochs=2,
        )
        
        print("\n" + "=" * 80)
        print("✅ PHASE 2 COMPLETE: Domestic-Trash Fine-tuning")
        print("=" * 80)
        
        final_model = 'runs/detect/trash_domestic_finetuned/weights/best.pt'
    else:
        final_model = 'runs/detect/trash_plastic_finetuned/weights/best.pt'
    
    print("\n\n" + "=" * 80)
    print("🎉 FINE-TUNING PIPELINE COMPLETE")
    print("=" * 80)
    print(f"\n📂 Final model: {final_model}")
    print("\n📊 Next Steps:")
    print("   1. Test on all datasets:")
    print("      python test.py --weights runs/detect/trash_plastic_finetuned/weights/best.pt")
    print("   2. Compare mAP50 on PLASTIC and weak classes vs original")
    print("   3. If improved, use as new best.pt")
    print("   4. Deploy for inference")
    
    print("\n💡 Tips for improvement:")
    print("   - Run multiple fine-tuning phases on different datasets")
    print("   - Monitor class-wise metrics (not just overall mAP50)")
    print("   - Use test set to validate on weak classes")
