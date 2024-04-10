import os
import csv
import requests
from bs4 import BeautifulSoup
from googlesearch import search

# Read bird names from the CSV file
def read_bird_names_from_csv(csv_file):
    bird_names = []
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        bird_names = [row[-1] for row in csv_reader]

    return bird_names

# Search Google for images of a bird
def search_google_images(bird_name, num_images=5):
    query = f"{bird_name} bird"
    search_results = search(query, num_results=num_images, lang="en")
    return search_results

# Download images from the search results
def download_images(search_results, output_dir,bird_names):
    for i, url in enumerate(search_results):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                image_path = os.path.join(output_dir, f"{i+1}.jpg")
                print("Image  Path:")
                print(image_path)
                with open(image_path, 'wb') as img_file:
                    img_file.write(response.content)
                print(f"Downloaded image {i+1} for {bird_names[i]}")
        except Exception as e:
            print(f"Error downloading image {i+1}: {str(e)}")

# Main function
def main(csv_file, output_dir):
    bird_names = read_bird_names_from_csv(csv_file)
    for bird_name in bird_names:
        search_results = search_google_images(bird_name)
        print(search_results[1:10])
        # download_images(search_results, output_dir, bird_names)

# Set the CSV file and output directory
csv_file = "bird_names.csv"
output_dir = "bird_images"

# # Create the output directory if it doesn't exist
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

# # Run the main function\
main(csv_file, output_dir)

# # Print a success message
# print(f"Images downloaded and saved in {output_dir}")
