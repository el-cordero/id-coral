

# import packages
from bs4 import BeautifulSoup 
import requests
import json
import re
import pandas as pd 

# website URL
url = 'http://www.coralsoftheworld.org/species_factsheets/'

# request website data
response = requests.get(url)

# parse through html file and select the ID
html = response.text
soup = BeautifulSoup(html, 'html.parser')
items = soup.select('option[value]')

# this deletes the first row which is not a coral species
del items[0] 

# gather coral species names
coral_species = [species.text for species in items]

# websites where individual coral species information can be found
coral_website = 'http://www.coralsoftheworld.org/species_factsheets/species_factsheet_summary/'

# edit the website name by adding genus-species
coral_sites = [coral_website + coral_site.lower().replace(' ','-') + '/' for coral_site in coral_species]

# create a function for where the coral image where be downloaded
def image_download_path(file_path, file_name, file_number):
    full_path = file_path + file_name + ' ' + str(file_number) + '.jpg'
    return full_path

# define a function for requesting each image within a coral website
def download_coral_images(coral_site,species_name,images_website_path,local_path):

    # request coral species website
    response = requests.get(coral_site)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # extract the script element that contains 'var gallery ='
    script_content = ''
    for script in soup.find_all('script'):
        if 'var gallery =' in script.text:
            script_content = script.text
            break
    
    # retrieve everything within the brackets
    match = re.match(r"[^[]*\[([^]]*)\]", script_content).groups()[0]
    json_string = '[' + match + ']'

    # transform the JSON to dataframe
    data = json.loads(json_string)
    df = pd.DataFrame(data)
    
    # retrieve urls for images
    image_url_full = []
    for string in df.image_url:
        image_url = string.rstrip('/').lstrip('/image')
        image_url = images_website_path + image_url + '.jpg'
        image_url_full.append(image_url)

    # request images from each url
    for i in range(0,len(image_url_full)):
        
        # request image url
        image_response = requests.get(image_url_full[i])

        # create file name
        file_name = image_download_path(local_path, species_name, i)

        # download the file
        if image_response.status_code == 200:
            # Open a local file with wb (write binary) permission
            with open(file_name, "wb") as file:
                for chunk in image_response.iter_content(chunk_size=128):
                    file.write(chunk)
            print("Image successfully downloaded: " + species_name + ' ' + str(i))
        else:
            print("Error downloading the image")

    # return the number of images as a count
    image_count = len(image_url_full)
    return image_count

# website path
images_website_path = 'http://www.coralsoftheworld.org/media/images/'
local_path = '/Users/EC13/Documents/Projects/Coral Reefs/Webscraping/downloads/'

# create a database of the species and number of images

species_image_count = []
for i in range(0,len(coral_species)):
    images_count = download_coral_images(coral_sites[i],coral_species[i],images_website_path,local_path)
    species_image_count.append(images_count)

# unlist the elements (which are lists)
species_images = sum(species_image_count,[])

# create pandas df
zipped = list(zip(coral_species,coral_sites,species_images))
species_info = pd.DataFrame(zipped, columns=['Scientific_Name','Website','Images'])

# save df
species_info_file = '/Users/EC13/Documents/Projects/Coral Reefs/Webscraping/info/Corals of the World.csv'
species_info.to_csv(species_info_file, sep='\t')
