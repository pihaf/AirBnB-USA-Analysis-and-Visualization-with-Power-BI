import requests
import os
import shutil
import gzip
from bs4 import BeautifulSoup
import pandas as pd

url = "https://insideairbnb.com/get-the-data/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

h3_tags = soup.find_all('h3')
tables = soup.find_all('table')

os.makedirs("data", exist_ok=True)

for h3, table in zip(h3_tags, tables):
    if "United States" not in h3.text:
        continue
    directory_name = h3.text.strip()
    print(directory_name)
    directory_path = os.path.join("data", directory_name)
    os.makedirs(directory_path, exist_ok=True)

    print(directory_path)
    
    print(f"Downloading files for {directory_name}...")
    
    a_tags = table.find_all("a")
    for a in a_tags:
        file_url = a.get('href')
        if not file_url:
            continue
        
        downloaded_file = a.text
        file_name = ''
        if downloaded_file == 'listings.csv':
            file_name = 'listings_summary.csv'
        elif downloaded_file == 'listings.csv.gz':
            file_name = 'listings_full.csv'
        elif downloaded_file == 'reviews.csv':
            file_name = 'reviews.csv'
        elif downloaded_file == 'neighbourhoods.csv':
            file_name = 'neighbourhoods.csv'
        else:
            continue

        file_path = os.path.join(directory_path, downloaded_file)
        print("Input file: ",file_path)

        # Download the file
        response = requests.get(file_url)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        # If the file is a .gz file, unzip it
        if downloaded_file.endswith('.gz'):
            # Specify the path where you want to save the decompressed file
            decompressed_file_path = os.path.join(directory_path, file_name)
            print("Output file: ", decompressed_file_path)
            
            # Open the .gz file for reading and the decompressed file for writing
            with gzip.open(file_path, 'rb') as f_in:
                with open(decompressed_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Remove the compressed file
            os.remove(file_path)
