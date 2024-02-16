import os
import numpy as np
from shutil import copy2
from sklearn.model_selection import train_test_split
import pandas as pd

# Paths
source_dir = '/Users/EC13/Documents/Projects/Coral Reefs/Webscraping/data/images/raw'
dest_dir = '/Users/EC13/Documents/Projects/Coral Reefs/Webscraping/data/images'

# Ratios
train_ratio = 0.7
test_ratio = 0.30
# validation_ratio = 0.15
# test_ratio = 0.15

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
list_dir.sort()

no_validation = []
no_images = []

for class_dir in list_dir:
    class_path = os.path.join(source_dir, class_dir)
    images = os.listdir(class_path)

    # Split dataset
    if len(images) > 1:
        train, test = train_test_split(images, test_size=test_ratio, random_state=42)
            # # Copy files to respective directories
        copy_files(train, 'train', source_dir, class_dir, dest_dir)
        copy_files(test, 'test', source_dir, class_dir, dest_dir)

        if len(train) > 1:
            train, val = train_test_split(train, test_size=0.5, random_state=42)
            copy_files(val, 'validation', source_dir, class_dir, dest_dir)
        else:
            no_validation.append(class_dir)
    else:
        no_images.append(class_dir)
        list_dir.pop(list_dir.index(class_dir))


    print(f'This directory does not have more than 1 file: {class_path}')


# Writing to a file
info_file = '/Users/EC13/Documents/Projects/Coral Reefs/Webscraping/data/images'

# Join the list items into a single string separated by commas
no_images_string = ', '.join(no_images)
no_validation_string = ', '.join(no_validation)
info_string_01 = f'Only one image contained in the {no_images_string} folder(s) - no test, train, validation splits created.\n\n' 
info_string_02 = f'Not enough images contained in the {no_validation_string} folder(s) - only test and train splits created.\n\n'


# Write the string to the file
with open(os.path.join(info_file,'info.txt'), 'w') as file:
    file.write(info_string_01 + info_string_02)

with open(os.path.join(info_file,'info_no_val.txt'), 'w') as file:
    file.write(no_validation_string)

with open(os.path.join(info_file,'info_no_split.txt'), 'w') as file:
    file.write(no_images_string)