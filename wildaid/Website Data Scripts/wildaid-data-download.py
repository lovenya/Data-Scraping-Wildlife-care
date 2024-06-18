import os
import requests
import pandas as pd

# Load the data from the Excel file
file_path = r"D:\AI-ML\Data Scraping\wwf\Data Excels (Main Data, Shortened Excel)\wwf-data-cleaned-shortened.xlsx"
data = pd.read_excel(file_path)

# Create directories if they don't exist
text_folder = 'wwf-text-files'
image_folder = 'wwf-images'
os.makedirs(text_folder, exist_ok=True)
os.makedirs(image_folder, exist_ok=True)

# Function to download images
def download_image(url, path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

# Function to sanitize unique_id
def sanitize_unique_id(unique_id):
    return unique_id.replace('-', '_')

# Iterate through the data
for index, row in data.iterrows():
    unique_id = sanitize_unique_id(str(row['unique_id']))
    text_content = row['article-post-text']
    image_url = row['article-post-image-src']
    
    # Ensure text content is a string, replace NaN with an empty string
    if pd.isna(text_content):
        text_content = ''
    
    # Create and write text file
    text_file_path = os.path.join(text_folder, f'{unique_id}.txt')
    with open(text_file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(text_content)
    
    # Download and save images
    if pd.notna(image_url):
        image_extension = os.path.splitext(image_url)[1].split('?')[0]
        image_file_path = os.path.join(image_folder, f'{unique_id}{image_extension}')
        download_image(image_url, image_file_path)

print("Script completed successfully.")
