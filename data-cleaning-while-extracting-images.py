import pandas as pd
import re

# Correct the file path by using double backslashes or raw string
file_path = r"C:\Users\loven\Downloads\jagran-wildlife-crime-hindi-scraper (3).xlsx"

# Load the data from the provided Excel file
df = pd.read_excel(file_path)


# Function to extract the image src link
def extract_image_src(text):
    match = re.search(r'src="([^"]+)"', text)
    return match.group(1) if match else None


# Apply the function to the article-link column and create a new column
df["article-post-image-src"] = df["article-link"].apply(extract_image_src)


# Step 1: Remove serial order number
df["unique_id"] = df["web-scraper-order"].apply(lambda x: x.split("-")[0])

# Step 2: Concatenate multiple rows of `article-post-text` for the same post
df_text_concat = df.groupby("unique_id", as_index=False).agg(
    {
        "web-scraper-start-url": "first",
        "article-link": "first",
        "article-link-href": "first",
        "article-title": "first",
        "article-post-text": lambda x: " ".join(x.dropna()),  # Concatenate text
        "article-post-image-src": lambda x: list(
            x.dropna()
        ),  # Collect images in a list
    }
)

# Step 3: Expand rows for multiple images and update unique_id with serial number
rows = []
for _, row in df_text_concat.iterrows():
    images = row["article-post-image-src"]
    if isinstance(images, list) and images:
        for i, image in enumerate(images):
            new_row = row.copy()
            new_row["unique_id"] = f"{row['unique_id']}-{i+1}"
            new_row["article-post-image-src"] = image
            if i > 0:
                new_row["web-scraper-start-url"] = None
                new_row["article-link"] = None
                new_row["article-link-href"] = None
                new_row["article-title"] = None
                new_row["article-post-text"] = None
            rows.append(new_row)
    else:
        row["unique_id"] = f"{row['unique_id']}-1"
        row["article-post-image-src"] = None
        rows.append(row)

# Create a new DataFrame from the expanded rows
df_cleaned = pd.DataFrame(rows)

# Save the cleaned DataFrame to a new Excel file
output_path = r"C:\Users\loven\Downloads\jagran-wildlife-crime-hindi-scraper-image-links-extracted-test.xlsx"
df_cleaned.to_excel(output_path, index=False)

print(f"Cleaned data saved to: {output_path}")
