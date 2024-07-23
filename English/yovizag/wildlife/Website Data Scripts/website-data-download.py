import os
import requests
import pandas as pd

# Load the data from the Excel file
file_path = r"D:\AI-ML\Data-Scraping-Wildlife-care\English\yovizag\Data Excels (Main Data, Shortened Excel)\yovizag-wildlife-shortened.xlsx"
data = pd.read_excel(file_path)

# Create directories if they don't exist
text_folder = "yovizag-wildlife-text-files"
image_folder = "yovizag-wildlife-images"
os.makedirs(text_folder, exist_ok=True)
os.makedirs(image_folder, exist_ok=True)


# Function to download images
def download_image(url, path, timeout=30):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=timeout)
        response.raise_for_status()
        if (
            "Content-Type" in response.headers
            and "image" in response.headers["Content-Type"]
        ):
            with open(path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded {path}")
        else:
            print(f"URL does not contain an image: {url}")
    except requests.exceptions.Timeout:
        print(f"Timeout while trying to download {url}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")


# Function to sanitize unique_id
def sanitize_unique_id(unique_id):
    return unique_id.replace("-", "_")


# Function to ensure URLs are complete
def complete_url(url):
    if url.startswith("//"):
        return "https:" + url
    return url


# Iterate through the data
for index, row in data.iterrows():
    unique_id = sanitize_unique_id(str(row["unique_id"]))
    text_content = row["article-post-text"]
    image_url = row["article-post-image-src"]

    # Debug prints
    print(f"\nProcessing row {index + 1}/{len(data)}")
    print(f"Unique ID: {unique_id}")
    print(f"Image URL: {image_url}")

    # Ensure text content is a string, replace NaN with an empty string
    if pd.isna(text_content):
        text_content = ""

    # Create and write text file
    text_file_path = os.path.join(text_folder, f"{unique_id}.txt")
    with open(text_file_path, "w", encoding="utf-8") as text_file:
        text_file.write(text_content)
        print(f"Text file created: {text_file_path}")

    # Download and save images
    if pd.notna(image_url):
        # Ensure the URL is complete
        image_url = complete_url(image_url)

        # Check if the URL ends with .gif or any other unsupported format
        if image_url.lower().endswith(".gif"):
            print(f"Skipping GIF image: {image_url}")
            continue
        image_extension = os.path.splitext(image_url)[1].split("?")[0]
        image_file_path = os.path.join(image_folder, f"{unique_id}{image_extension}")
        print(f"Downloading image from: {image_url} to {image_file_path}")
        download_image(image_url, image_file_path)

print("Script completed successfully.")
