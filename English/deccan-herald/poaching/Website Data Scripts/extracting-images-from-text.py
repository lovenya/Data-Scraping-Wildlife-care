import pandas as pd
import re

# Load the Excel file
file_path = r"D:\AI-ML\Data-Scraping-Wildlife-care\English\deccan-herald\poaching\Data Excels (Main Data, Shortened Excel)\deccan-herald-poaching-cleaned.xlsx"
df = pd.read_excel(file_path)


# Function to extract image URLs
def extract_image_url(text):
    if not isinstance(text, str):
        return None
    match = re.search(r'<img src="(.*?)"', text)
    return match.group(1) if match else None


# Function to clean the article-date column
def clean_article_date(date_text):
    return (
        date_text.replace("Last Updated : ", "").strip()
        if isinstance(date_text, str)
        else date_text
    )


# Iterate over the DataFrame and update the article-post-image-src column if it's blank
for index, row in df.iterrows():
    if pd.isna(row["article-post-image-src"]):
        image_url = extract_image_url(row["article-post-text"])
        if image_url:
            df.at[index, "article-post-image-src"] = image_url

# Save the updated DataFrame to a new Excel file
output_file_path = r"D:\AI-ML\Data-Scraping-Wildlife-care\English\deccan-herald\poaching\Data Excels (Main Data, Shortened Excel)\deccan-herald-poaching-cleaned-extracted.xlsx"
df.to_excel(output_file_path, index=False)

output_file_path
