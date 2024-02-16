from collections import defaultdict
import pandas as pd 
import os
import shutil


# Example list of file names
file_names = os.listdir('/Users/EC13/Documents/Projects/Coral Reefs/Webscraping/images')

# Initialize a defaultdict to group files
file_groups = defaultdict(list)

# Loop through each file name
for file_name in file_names:
    # Split the file name by spaces and remove the last element (the number)
    # to get the species name
    species_name = " ".join(file_name.split()[:-1])
    # Add the file name to the list of files for this species
    file_groups[species_name].append(file_name)

# Printing the grouped files
for species, files in file_groups.items():
    print(f"{species}: {len(files)}")
    print(f"{files}")

# Base directory where the new species folders will be created
# This should be an existing directory where you want to organize the files
base_dir = '/Users/EC13/Documents/Projects/Coral Reefs/Webscraping/data'

# Directory containing the original files
source_dir = '/Users/EC13/Documents/Projects/Coral Reefs/Webscraping/images'

# Ensure the base directory exists
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# Move each file into the species directory
def move_files(source_dir, species_dir, files):
    for file_name in files:
        source_path = os.path.join(source_dir, file_name)
        destination_path = os.path.join(species_dir, file_name)
        if os.path.exists(destination_path):
            print(f'{file_name} already moved')
        else:
            # Move the file
            shutil.move(source_path, destination_path)
    return(f'{file_name} complete')

for species, files in file_groups.items():
    # Create a directory for the species if it doesn't exist
    species_dir = os.path.join(base_dir, species)
    if not os.path.exists(species_dir):
        os.makedirs(species_dir)
    
    move_files(source_dir,species_dir,files)

print("Files have been organized into species directories.")


# out_path = '/Users/EC13/Documents/Projects/Coral Reefs/Webscraping/data'
# for species, files in file_groups.items():

#     # Move each file into the species directory
#     for file_name in files:
#         data_path = os.path.join(out_path,species, file_name)
#         if os.path.exists(data_path):
#             new_path = data_path + '.jpg'
#             # Move the file
#             shutil.move(data_path, new_path)
