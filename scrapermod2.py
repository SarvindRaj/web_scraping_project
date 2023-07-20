import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse

# Create a BeautifulSoup object
def make_soup(url, source_url=None):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the GET request was unsuccessful
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
        print(f"Failed to access {url}")
        print(f"This link was found on {source_url}")
        return None

# Recursive function to extract links
def follow_links(url, visited, source_url=None):
    if url not in visited:
        visited.add(url)

        # Define parsed_url here
        parsed_url = urlparse(url)
        # Extract the school_name
        school_name = parsed_url.path.split('/')[2]

        soup = make_soup(url, source_url)
        if soup is None:  # Skip this URL if we couldn't get its content
            return

        # rest of the code
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

            if urlparse(href).netloc == parsed_url.netloc:
                follow_links(href, visited, url)  # pass the current URL as the source URL for the next level


# Define the URL we're scraping
urls = [
    "https://sites.google.com/moe-dl.edu.my/skttdijayaskk/id-google-classroom-murid",
    "https://sites.google.com/moe-dl.edu.my/smkss/home"
]

keywords = ['id delima', 'delima', 'google classroom id', 'id', 'ID MOE']

visited = set()  # To keep track of visited pages

# Prepare the CSV file
with open('outputmod2.csv', 'w', newline='') as csvfile:
    fieldnames = ['Source Website', 'URL', 'Link Text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for url in urls:
        follow_links(url, visited)
