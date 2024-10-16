import requests
import PyPDF2
import io
import json
import os

# Function to download the PDF content from a URL
def download_pdf(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises error for bad status codes
    return response.content

# Function to convert PDF content into text
def pdf_to_text(pdf_content):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to process the JSON file, download PDFs, and save the text
def process_json_and_save_text(json_file, output_dir="text"):
    # Load the JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through each item in the JSON
    for item in data:
        url = item['link']
        communique_no = item['communique_no']
        print(f"Processing {communique_no} from {url}...")

        try:
            # Download and convert PDF to text
            pdf_content = download_pdf(url)
            text_content = pdf_to_text(pdf_content)

            # Save the text content to a file
            text_file_path = os.path.join(output_dir, f"{communique_no}.txt")
            with open(text_file_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text_content)

            print(f"Saved {communique_no} as {text_file_path}")

        except Exception as e:
            print(f"Failed to process {communique_no}: {str(e)}")

if __name__ == "__main__":
    # Define the input JSON file and output directory
    json_file = "../circulars/cdsl/index.json"
    output_dir = "text"

    # Process the JSON and save the PDFs as text
    process_json_and_save_text(json_file, output_dir)
