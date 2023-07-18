import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse

# Create a BeautifulSoup object
def make_soup(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception if the GET request was unsuccessful
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# Define the URL we're scraping
urls = [
    "https://sites.google.com/moe-dl.edu.my/skttdijayaskk/id-google-classroom-murid",
    "https://sites.google.com/moe-dl.edu.my/smkss/home"
]

keywords = ['id delima', 'delima', 'google classroom id', 'id', 'ID MOE']

# Prepare the CSV file
with open('output.csv', 'w', newline='') as csvfile:
    fieldnames = ['Source Website', 'URL', 'Link Text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for url in urls:
        # Pass the URL to BeautifulSoup
        soup = make_soup(url)

        # Find the school name
        parsed_url = urlparse(url)
        school_name = parsed_url.path.split('/')[2]

        # Find and print all 'a' tags (which define hyperlinks) in the HTML
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is None:
                continue  # Skip this link if it has no href

            # Prepend base URL if the URL is a relative URL
            if href.startswith("/"):
                href = f"https://sites.google.com{href}"

            text = link.text.lower()
            if 'https://lookerstudio.google.com/' in href or any(keyword in text for keyword in keywords):
                writer.writerow({'Source Website': school_name, 'URL': href, 'Link Text': text})
