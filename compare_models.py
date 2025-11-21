"""
Test script to analyze performance on weak classes (plastic, etc.)
and compare original vs fine-tuned model
"""

from ultralytics import YOLO
import os

def test_model(model_path, dataset_path, model_name):
    """Test a model and report metrics"""
    print(f"\n{'='*80}")
    print(f"Testing: {model_name}")
    print(f"{'='*80}")
    
    model = YOLO(model_path)
    
    results = model.val(
        data=dataset_path,
        imgsz=640,
        batch=16,
        verbose=True
    )
    
    print(f"\n✅ Results for {model_name}:")
    print(f"   mAP50: {results.results_dict.get('metrics/mAP50(B)', 'N/A')}")
    print(f"   mAP50-95: {results.results_dict.get('metrics/mAP50-95(B)', 'N/A')}")
    
    return results

if __name__ == '__main__':
    print("\n" + "="*80)
    print("COMPARING MODELS: Original vs Fine-tuned")
    print("="*80)
    
    # Model paths
    original_model = 'runs/detect/trash_model/weights/best.pt'
    finetuned_model = 'runs/detect/trash_plastic_finetuned/weights/best.pt'
    
    # Test datasets
    test_configs = [
        ('data/GARBAGE-CLASSIFICATION-3-2/data.yaml', 'GARBAGE-CLASSIFICATION (Plastic Focus)'),
        ('data/Domestic-Trash--1/data.yaml', 'Domestic-Trash (Household)'),
        ('data/garbage_best-1/data.yaml', 'Garbage-Best'),
    ]
    
    print("\n🔍 Testing on different datasets...\n")
    
    for dataset_path, dataset_name in test_configs:
        if os.path.exists(dataset_path):
            print(f"\n\n📊 Dataset: {dataset_name}")
            print(f"Path: {dataset_path}")
            
            # Test original
            if os.path.exists(original_model):
                results_orig = test_model(original_model, dataset_path, "Original Model (best.pt)")
            else:
                print(f"❌ Original model not found: {original_model}")
            
            # Test fine-tuned
            if os.path.exists(finetuned_model):
                results_ft = test_model(finetuned_model, dataset_path, "Fine-tuned Model")
            else:
                print(f"⚠️  Fine-tuned model not yet available")
        else:
            print(f"\n❌ Dataset not found: {dataset_path}")
    
    print("\n\n" + "="*80)
    print("📈 ANALYSIS COMPLETE")
    print("="*80)
    print("\n💡 Key metrics to check:")
    print("   - PLASTIC class performance increase")
    print("   - CARDBOARD, PAPER, GLASS class improvements")
    print("   - Overall mAP50 vs fine-tuned mAP50")
    print("   - Generalization (performance on other datasets)")
