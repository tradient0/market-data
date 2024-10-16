import requests
import PyPDF2
import io
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

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

# Function to process a single PDF: download it, extract text, and save the result
def process_single_pdf(item, output_dir):
    try:
        url = item["circFilelink"]
        circ_number = item["circNumber"]
        print(f"Processing {circ_number} from {url}...")

        # Download the PDF and convert to text
        pdf_content = download_pdf(url)
        text_content = pdf_to_text(pdf_content)

        # Save the text content to a file
        text_file_path = os.path.join(output_dir, f"{circ_number}.txt")
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text_content)

        print(f"Saved {circ_number} as {text_file_path}")
        return True  # Success
    except Exception as e:
        print(f"Failed to process {item['circNumber']}: {str(e)}")
        return False  # Failure

# Function to process the JSON file, download PDFs, and save the text
def process_json_and_save_text(json_file, output_dir="circulars/nse/text", max_workers=5):
    # Load the JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # List to hold the futures for multi-threading
    futures = []

    # Use ThreadPoolExecutor to parallelize PDF processing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for item in data["data"]:
            # Process only if the file extension is pdf
            if item["fileExt"] == "pdf":
                # Submit the task to the thread pool
                futures.append(executor.submit(process_single_pdf, item, output_dir))

        # Wait for all the futures to complete
        for future in as_completed(futures):
            if future.result() is False:
                print("A task failed during processing.")

if __name__ == "__main__":
    # Define the input JSON file and output directory
    json_file = "circulars/nse/index.json"  # Path to the JSON file
    output_dir = "circulars/nse/text"  # Directory to save the text files

    # Process the JSON and save the PDFs as text, using multi-threading
    process_json_and_save_text(json_file, output_dir, max_workers=10)  # Adjust max_workers as needed
