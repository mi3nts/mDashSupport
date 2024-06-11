# ***************************************************************************
#   Macaulay Library Media Downloader
#   ---------------------------------
#   Written by: Lakitha Omal Harindha Wijeratne
#   - for -
#   Mints: Multi-scale Integrated Sensing and Simulation
#   ---------------------------------
#   Date: May 7th, 2024
#   ---------------------------------
#   This module is written to download bird pictures from the 
#   Macaulay Library - https://www.macaulaylibrary.org/ in support
#   of MINTS grafana dashbords
#   
#   --------------------------------------------------------------------------
#   https://github.com/mi3nts
#   http://utdmints.info/
#  ***************************************************************************


import requests
import os
import yaml
import json 
import pandas as pd 
import time 
import logging


# TASKS 
# 1 Have a mints defenitions file to keep audio, video and images folder for all birds 
# 2 Have a credentials file to keep 
# 3 Have a list of all birds in texas 
# 4 Using the said list download all bird pictures with the highest rating and with the proper aspect ratio
# 5 Download the best quality audio video of the said birds 


# Things to do - Add pic, audio, video fodlers to the code 
credentialsFile      = 'credentials.yaml'
credentials          = yaml.load(open(credentialsFile))


api_key     = credentials['eBirdApiKey'] # Replace 'your_api_key' with your actual API key if needed
dataFolder  = credentials['dataFolder']

dataFolderPhoto = dataFolder + "/photo/"

# Define the base URL for the Macaulay Library API
base_url         = 'https://search.macaulaylibrary.org/api/v1/'
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


# Define the file path
file_path_labels = 'https://raw.githubusercontent.com/mi3nts/mDashSupport/main/resources/birdCalls/labels.csv'

# Read the CSV file into a DataFrame
df_labels_bird_call = pd.read_csv(file_path_labels)
# df_labels = pd.DataFrame.from_dict(data, orient='index', columns=['Species'])

# # Print the DataFrame
print(df_labels_bird_call)

# URL of the JSON file
url = "https://raw.githubusercontent.com/mi3nts/mDashSupport/main/resources/birdCalls/eBird_taxonomy_codes_2021E.json"

# Fetch JSON data from URL
response = requests.get(url)
data     = response.json()

# Convert JSON data to DataFrame
df_labels_taxonomy = pd.DataFrame.from_dict(data, orient='index', columns=['Species'])

# Reset index to use the default integer index
df_labels_taxonomy.reset_index(inplace=True)
df_labels_taxonomy.columns = ['Code', 'Species']

# Display the DataFrame
# print(df_labels_taxonomy)

def main():

    for index, row in df_labels_bird_call.iterrows():
        Scientific_Name = row['Scientific name']
        Common_Name = row['Common name']
        print("---------------------------------------------------------------")
        print(f"Scientific Name: {Scientific_Name}")
        print(f"Common Name: {Common_Name}")
        species_name = Scientific_Name +"_" +Common_Name
        
        # species_name = "Common Ostrich"
        code = get_code_for_species(species_name, df_labels_taxonomy)
        if code:
            try:
                print(f"The code for {species_name} is {code}.")
                url = "https://search.macaulaylibrary.org/api/v1/search"

                # Only Dowloads photos taken after 2000, and adult birds and rated from highest to lowest
                params = {
                    "taxonCode": code,
                    "mediaType": "photo",
                    "age": "adult",
                    "beginYear": 2000,
                    "sort": "rating_rank_desc"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    content = data['results']['content']
                    for item in content:
                        if item['width'] is not None and item['height'] is not None:
                            if item['width']/ item['height']< 1.55 and  item['width']/ item['height']> 1.45 and item['width']>3000 :
                                response = requests.get(item['largeUrl'])
                                # Check if the request was successful (status code 200)
                                if response.status_code == 200:
                                    # Open a file in binary write mode and write the content of the response to it
                                    with open(dataFolderPhoto+ item['commonName'] + ".jpeg", "wb") as file:
                                        file.write(response.content)
                                    print("Image downloaded successfully.")
                                else:
                                    print("Failed to download the image. Status code:", response.status_code)
                                break;
                                    
                else:
                    print("Error:", response.status_code)
                    time.sleep(5)
            except Exception as e:
                logging.error("An error occurred: %s for bird %b", e,code)
                print("An error occurred. Please check the log file for more details.")

        else:
            print(f"No code found for {species_name}.")
    # df_ebird_taxonomy_labels_json = json.load(ebird_taxonomy_labels)



def get_code_for_species(species_name, df):
    """
    Get the code for a given species from the DataFrame.
    
    Parameters:
        species_name (str): The name of the species.
        df (DataFrame): The DataFrame containing the species codes.
        
    Returns:
        str: The code for the given species.
        None: If the species is not found in the DataFrame.
    """
    row = df[df['Species'] == species_name]
    if not row.empty:
        return row['Code'].iloc[0]
    else:
        return None
    

if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    print("Downloading Photos fron Macaulay Library  to " + dataFolder )
    main()    