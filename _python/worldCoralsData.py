
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

scientific_name = []
detail = []
geographical_origin = []
creator = []
image_url = []
image_label = []

for i in range(0,len(coral_sites)):
    response = requests.get(coral_sites[i])
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    script_content = ''
    for script in soup.find_all('script'):
        if 'var gallery =' in script.text:
            script_content = script.text
            break

    match = re.match(r"[^[]*\[([^]]*)\]", script_content).groups()[0]
    json_string = '[' + match + ']'

    data = json.loads(json_string)
    df = pd.DataFrame(data)

    for j in range(0,len(df)):
        # Parse the string using BeautifulSoup
        caption = BeautifulSoup(df.caption[j], 'html.parser')

        # Extract details by class name
        scientific_name.append(caption.find('span', class_='caption_scientific_name').text)
        detail.append(caption.find('span', class_='caption_detail').text)
        geographical_origin.append(caption.find('span', class_='caption_geographical_origin').text)
        creator.append(caption.find('span', class_='caption_creator').text)
        image_url.append(df.image_url[j])
        image_label.append(j)
    print(scientific_name[i])

# create a dataframe
image_labels = [] 
for i in range(0,len(image_label)):
    label = scientific_name[i] + ' ' + str(image_label[i])
    image_labels.append(label)

len(image_labels)
image_url

zipped = zip(scientific_name,image_label,geographical_origin,creator,detail,image_labels,image_url)

coral_data = pd.DataFrame(zipped)
coral_data.columns=['scientific_name','image_label','geographical_origin','creator','detail','image_labels','image_url']

images_website_path = 'http://www.coralsoftheworld.org/media/images/'
image_url_full = []
for string in coral_data.image_url:
    image_url_str = string.rstrip('/').lstrip('/image')
    image_url_str = images_website_path + image_url_str + '.jpg'
    image_url_full.append(image_url_str)

coral_data.image_url = image_url_full

creator_name = []
for string in coral_data.creator:
    creator_name.append(string.lstrip('Photograph: '))
coral_data.creator = creator_name

data_into_file = '/Users/EC13/Documents/Projects/Coral Reefs/Webscraping/info/CoralsoftheWorld_ImageData.csv'

coral_data.to_csv(data_into_file, sep=';')
# coral_data = pd.read_csv(data_into_file, sep=';')