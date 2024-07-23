import pandas as pd

# Specify the input file path
input_file_path = r"D:\AI-ML\Data-Scraping-Wildlife-care\English\wwf-india\Data Excels (Main Data, Shortened Excel)\wwf-india-cleaned.xlsx"

# Load the Excel file
df = pd.read_excel(input_file_path)

# Update the 'article-post-image-src' column
df["article-post-image-src"] = df["article-post-image-src"].apply(
    lambda x: "https:" + x if pd.notna(x) else x
)

# Save the updated DataFrame back to the same Excel file
df.to_excel(input_file_path, index=False)

# Print completion message
print(f"File has been successfully updated and saved to {input_file_path}")
