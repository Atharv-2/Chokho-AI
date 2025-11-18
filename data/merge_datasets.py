import os
import yaml
import shutil

target_classes = ['plastic', 'metal', 'paper', 'glass', 'organic', 'bin']

garbage_mapping = {
    'PLASTIC': 'plastic',
    'METAL': 'metal',
    'PAPER': 'paper',
    'CARDBOARD': 'paper',
    'GLASS': 'glass',
    'BIODEGRADABLE': 'organic',
}


roboflow_mapping = {
    'all' : 'plastic',
    'trash': 'plastic',
    'bin' :'bin'
}

def get_class_index(class_name , target_classes):
    try:
        return target_classes.index(class_name)
    except ValueError:
        return None
    

def  convert_label_file(input_path, output_path, old_classes, class_mapping, target_classes):
    if not os.path.exists(input_path):
        return False
    
    with open(input_path,'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 5:
            continue

        old_class_idx = int(parts[0])
        if old_class_idx >= len(old_classes):
            continue


        old_class_name = old_classes[old_class_idx]
        new_class_name = class_mapping.get(old_class_name)

        if new_class_name is None:
            continue

        new_class_idx = get_class_index(new_class_name, target_classes)
        if new_class_idx is None:
            continue

        parts[0] = str(new_class_idx)
        new_lines.append(' '.join(parts) + '\n')
    
    if new_lines:
        os.makedirs(os.path.dirname(output_path) , exist_ok=True)
        with open(output_path, 'w') as f:
            f.writelines(new_lines)
        return True

    return False

def process_dataset(dataset_path, output_path, split, old_classes, class_mapping, target_classes, dataset_name):
    img_input = os.path.join(dataset_path,split,'images')
    lbl_input = os.path.join(dataset_path, split, 'labels')

    img_output = os.path.join(output_path, split,'images')
    lbl_output = os.path.join(output_path,split, 'labels')

    os.makedirs(img_output, exist_ok=True)
    os.makedirs(lbl_output, exist_ok=True)

    if not os.path.exists(img_input):
        print(f"{dataset_name}/{split} not found")
        return 0;

    count = 0
    for img_file in os.listdir(img_input):
        if not img_file.endswith(('jpg', '.jpeg', '.png')):
            continue

        img_name = os.path.splitext(img_file)[0]
        lbl_file = img_name + '.txt'
        
        img_src = os.path.join(img_input, img_file)
        lbl_src = os.path.join(lbl_input, lbl_file)
        
        unique_img = f"{dataset_name}_{img_file}"
        unique_lbl = f"{dataset_name}_{img_name}.txt"
        
        img_dst = os.path.join(img_output, unique_img)
        lbl_dst = os.path.join(lbl_output, unique_lbl)

        if convert_label_file(lbl_src, lbl_dst, old_classes, class_mapping, target_classes):
            shutil.copy2(img_src, img_dst)
            count += 1
    
    return count

def merge_all_datasets(dataset_config, output_path):
    for split in ['train', 'valid', 'test']:
        os.makedirs(os.path.join(output_path,split,'images'), exist_ok=True)
        os.makedirs(os.path.join(output_path,split,'labels'), exist_ok= True)

    total_counts = {'train':0,'valid':0,'test':0}

    for config in dataset_config:
        print(f"Processing: {config['name']}")
        print(f"Original classes: {config['classes']}")

        for split in ['train', 'valid', 'test']:
            count = process_dataset(dataset_path=config['path'], output_path=output_path, split=split, old_classes=config['classes'], class_mapping=config['mapping'], target_classes=target_classes, dataset_name=config['name'])
            total_counts[split] += count
            print(f"{split} : {count} images")

    data_yaml = {
        'path': os.path.abspath(output_path),
        'train': 'train/images',
        'val': 'valid/images',
        'test': 'test/images',
        'nc': len(target_classes),
        'names': target_classes
    }   

    yaml_path = os.path.join(output_path, 'data.yaml')
    with open(yaml_path, 'w') as f:
        yaml.dump(data_yaml, f, default_flow_style=False)    

    print(f"   Train:  {total_counts['train']}")
    print(f"   Valid:  {total_counts['valid']}")
    print(f"   Test:   {total_counts['test']}")
    print(f"   TOTAL:  {sum(total_counts.values())}")


if __name__ == "__main__":
    with open('GARBAGE-CLASSIFICATION-3-2/data.yaml','r') as f:
        garbage_data = yaml.safe_load(f)
        garbage_classes = garbage_data['names']

    with open('IntelligentVision-7/data.yaml','r') as f:
        roboflow_data = yaml.safe_load(f)
        roboflow_classes = roboflow_data['names']

    datasets = [
        {
            'name':'garbage',
            'path':'GARBAGE-CLASSIFICATION-3-2',
            'classes': garbage_classes,
            'mapping': garbage_mapping
        },
        {
            'name':'roboflow',
            'path':'IntelligentVision-7',
            'classes' : roboflow_classes,
            'mapping': roboflow_mapping
        }
    ]

    merge_all_datasets(datasets, 'merged_chokho_dataset')