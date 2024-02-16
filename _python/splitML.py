import os
import numpy as np
from shutil import copy2
from sklearn.model_selection import train_test_split

# Paths
source_dir = '/Users/EC13/Documents/Projects/Coral Reefs/Webscraping/data/images/raw'
dest_dir = '/Users/EC13/Documents/Projects/Coral Reefs/Webscraping/data/images'

# Ratios
train_ratio = 0.6
validation_ratio = 0.20
test_ratio = 0.20

# Ensure destination subdirectories exist
for split in ['train', 'validation', 'test']:
    for class_dir in os.listdir(source_dir):
        os.makedirs(os.path.join(dest_dir, split, class_dir), exist_ok=True)


    # Function to copy files
def copy_files(files, split, source_dir, class_dir, dest_dir):
    for file in files:
        src_path = os.path.join(source_dir, class_dir, file)
        dest_path = os.path.join(dest_dir, split, class_dir, file)
        copy2(src_path, dest_path)
        
# Splitting
list_dir = os.listdir(source_dir)
list_dir.pop(list_dir.index('.DS_Store'))

for class_dir in list_dir:
    class_path = os.path.join(source_dir, class_dir)
    images = os.listdir(class_path)
    

    # Split dataset
    train_val, test = train_test_split(images, test_size=test_ratio, random_state=42)
    train, val = train_test_split(train_val, test_size=validation_ratio / (validation_ratio + train_ratio), random_state=42)



    # Copy files to respective directories
    copy_files(train, 'train', source_dir, class_dir, dest_dir)
    copy_files(val, 'validation', source_dir, class_dir, dest_dir)
    copy_files(test, 'test', source_dir, class_dir, dest_dir)

print("Dataset successfully split into training, validation, and testing sets.")
