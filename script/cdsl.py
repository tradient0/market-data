import json
from bs4 import BeautifulSoup

# Read the HTML content
with open('circulars/cdsl/cdsl_page.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table with the data
table = soup.find('table', {'id': 'table1'})

# Extract the data rows
data = []
rows = table.find('tbody').find_all('tr')

for row in rows:
    cols = row.find_all('td')
    if len(cols) >= 4:
        # Extract relevant data
        serial_no = cols[0].text.strip()
        communique_no = cols[1].text.strip()
        subject = cols[2].find('a').text.strip()
        date = cols[3].text.strip()
        # Construct the full URL for the link
        link = "https://www.cdslindia.com" + cols[2].find('a')['href'].replace('..', '')
        
        # Append the row data as a dictionary
        data.append({
            'serial_no': serial_no,
            'communique_no': communique_no,
            'subject': subject,
            'date': date,
            'link': link
        })

# Convert the data to JSON and save it to a file
with open('circulars/cdsl/index.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)
