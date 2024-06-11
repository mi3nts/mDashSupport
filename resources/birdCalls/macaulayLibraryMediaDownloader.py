

# ***************************************************************************
#   Macaulay Library Media Downloader
#   ---------------------------------
#   Written by: Lakitha Omal Harindha Wijeratne
#   - for -
#   Mints: Multi-scale Integrated Sensing and Simulation
#   ---------------------------------
#   Date: May 7th, 2024
#   ---------------------------------
#   This module is written for generic implimentation of MINTS projects
#   --------------------------------------------------------------------------
#   https://github.com/mi3nts
#   http://utdmints.info/
#  ***************************************************************************


import requests
import os
import yaml
import sys
# TASKS 
# 1 Have a mints defenitions file to keep audio, video and images folder for all birds 
# 2 Have a credentials file to keep 
# 3 Have a list of all birds in texas 
# 4 Using the said list download all bird pictures with the highest rating and with the proper aspect ratio
# 5 Download the best quality audio video of the said birds 

credentialsFile      = 'credentials.yaml'

# Define the base URL for the Macaulay Library API
base_url    = 'https://search.macaulaylibrary.org/api/v1/'

credentials = yaml.load(open(credentialsFile))

api_key     = credentials['eBirdApiKey'] # Replace 'your_api_key' with your actual API key if needed

print(api_key)

# sys.wget("https://cdn.download.ams.birds.cornell.edu/api/v1/asset/618625751/1200")
# # Define the headers with your API key
# headers = {
#     'Authorization': f'Bearer {api_key}' if api_key else None
# }

import requests

# URL of the file to be downloaded
url = "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/618625751/1200"

# Send a GET request to the URL
response = requests.get(url)

# Save the file
file_path = "bird_image.jpg"
with open(file_path, 'wb') as file:
    file.write(response.content)

print(f"File saved to {file_path}")
# Since this works we need to figure out the asset number from the api


# Reading the Birdcall list 
import pandas as pd

# Replace 'your_file.csv' with the path to your CSV file
df = pd.read_csv('https://raw.githubusercontent.com/mi3nts/mDashSupport/main/resources/birdCalls/labels/labels.csv')

# Display the first few rows of the DataFrame
print(df.head())



import requests

def get_taxonomy_code(scientific_name):
    url = "https://www.itis.gov/ITISWebService/jsonservice/searchByScientificName"
    params = {"srchKey": scientific_name}
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data["scientificNames"]:
        return data["scientificNames"][0]["tsn"]
    else:
        return None

scientific_name = "Mimus polyglottos"
taxonomy_code = get_taxonomy_code(scientific_name)
print(f"The taxonomy code for {scientific_name} is {taxonomy_code}.")

# The Kind of link that we are looking for 
# https://search.macaulaylibrary.org/api/v1/search?&taxonCode=normoc&mediaType=photo&age=adult&beginYear=2020&endYear=2024&sort=rating_rank_desc
# The challenge is to get the taxinomic code 


url = "https://search.macaulaylibrary.org/api/v1/search"
params = {
    "taxonCode": "normoc",
    "mediaType": "photo",
    "age": "adult",
    "beginYear": 2020,
    "endYear": 2024,
    "sort": "rating_rank_desc"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    # Do something with the data
    print(data)
else:
    print("Error:", response.status_code)



# # Define the common name of the bird you want to search for
# common_name = 'specific_bird_name'  # Replace 'specific_bird_name' with the bird's common name

# # Create the search URL with filtering options for exact common name match
# # We use the `&q=` parameter to search for the exact common name
# search_url = f'{base_url}/search?&mediaType=Photo&&regionCode=US-TX'

# # Make a request to the Macaulay Library API
# response = requests.get(search_url, headers=headers)


# print(response.text)
# Check if the request was successful
# if response.status_code == 200:
#     # Parse the JSON response
#     data = response.json()
#     first_result = data['results']
#     print(first_result)
#     # Check if there are results
#     if data.get('results'):
#         # Get the first image URL from the results
#         first_result = data['results'][0]
#         image_url = first_result.get('assets', [{}])[0].get('file')

#         if image_url:
#             # Download the image
#             image_response = requests.get(image_url)

#             # Define the file path for saving the image
#             bird_name_safe = common_name.replace(' ', '_')  # Replace spaces with underscores for filename
#             file_path = os.path.join(os.getcwd(), f"{bird_name_safe}.jpg")

#             # Save the image to the file path
#             with open(file_path, 'wb') as file:
#                 file.write(image_response.content)

#             print(f"Image of '{common_name}' downloaded to {file_path}")
#         else:
#             print(f"No image found for {common_name}")
#     else:
#         print(f"No results found for {common_name}")
# else:
#     print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
