import pandas as pd

# Specify the input file path
input_file_path = r"D:\AI-ML\Data-Scraping-Wildlife-care\Marathi\agrovon-esakal-wildlife\Data Excels (Main Data, Shortened Excel)\agrovon-esakal-wildlife-marathi-cleaned.xlsx"

# Specify the output file path
output_file_path = r"D:\AI-ML\Data-Scraping-Wildlife-care\Marathi\agrovon-esakal-wildlife\Data Excels (Main Data, Shortened Excel)\agrovon-esakal-wildlife-marathi-cleaned-sanitized.xlsx"

# Load the Excel file
df = pd.read_excel(input_file_path)

# Update the 'article-post-image-src' column
df["article-post-image-src"] = df["article-post-image-src"].apply(
    lambda x: "https:" + x if pd.notna(x) else x
)

# Save the updated DataFrame to a new Excel file
df.to_excel(output_file_path, index=False)

# Print completion message
print(f"File has been successfully sanitized and saved to {output_file_path}")
