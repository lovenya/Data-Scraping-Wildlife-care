import pandas as pd

# Specify the input file path
input_file_path = r"D:\AI-ML\Data-Scraping-Wildlife-care\English\iccwc\Data Excels (Main Data, Shortened Excel)\iccwc-data-cleaned.xlsx"

# Load the Excel file
df = pd.read_excel(input_file_path)

# Define the base URL
base_url = "https://iccwc-wildlifecrime.org/"


# Update the 'article-post-image-src' column
def update_image_src(src):
    if pd.notna(src):
        if src.startswith("/sites"):
            return base_url + src[1:]
        elif src.startswith("data:image"):
            return ""
    return src


df["article-post-image-src"] = df["article-post-image-src"].apply(update_image_src)

# Save the updated DataFrame back to the same Excel file
df.to_excel(input_file_path, index=False)

# Print completion message
print(f"File has been successfully updated and saved to {input_file_path}")
