
import os
from PIL import ImageFile, Image
ImageFile.LOAD_TRUNCATED_IMAGES = True

import glob



file_path = r'/Users/EC13/Documents/Projects/Coral Reefs/Webscraping/downloads/'

image_files = os.listdir(file_path)
image_files.sort()

image_files.pop(image_files.index('.DS_Store'))

image_file_path = [file_path + '/' + file for file in image_files]

output_path = r'/Users/EC13/Documents/Projects/Coral Reefs/Webscraping/images'
images_out = [output_path + '/' + file for file in image_files]

# for i in range(0,len(image_files)):
#     original_image = Image.open(image_file_path[i])
#     original_image.save(images_out[i],'JPEG', optimize=True,quality=50)
#     print("Image compressed and saved.")


def process_image(file_path, output_path):
    # Open an image file
    with Image.open(file_path) as img:
        width, height = img.size
        # Optionally, resize the image if it's too large
        # Example: resize if either dimension is greater than 1000px
        if width > 1000 or height > 1000:
            img = img.resize((width // 2, height // 2))

        # Attempt to reduce file size by decreasing the quality
        quality = 95  # Starting quality
        while quality > 5:
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            if os.path.getsize(output_path) < 10240:  # Less than 10 KB
                break
            quality -= 5  # Decrease quality to further reduce file size

for i in range(0,len(image_file_path)):
    with image_file_path[i].lower() as img:
        if img.endswith('.jpg') or img.endswith('.jpeg'):
            process_image(img, images_out[i])

