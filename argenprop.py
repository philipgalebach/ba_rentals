import random
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import csv
import time  # To add delays between requests for ethical scraping

# Define the CSV file path
csv_file_path = './apartment_listings.csv'

# Define the fieldnames for the CSV
fieldnames = ['price', 'expenses', 'address', 'size', 'bedrooms', 'bathrooms', 'url', 'listing_url']

# Define patterns to search for the needed information
patterns = {
    'expenses': r'\+\s*\$\s*([\d\.]+)\s*expensas',
    'address': r'class="card__address"[^>]*>\s*([^<]+)',
    'size': r'(\d+)\s*m²\s*cubie',
    'bedrooms': r'(\d+)\s*dorm',
    'bathrooms': r'(\d+)\s*baños'
}

s = HTMLSession()

base_url = 'https://www.argenprop.com'
url = base_url + '/inmuebles/alquiler/capital-federal-o-recoleta/3-dormitorios?'

def getdata(url):
    r = s.get(url)
    r.html.render(sleep=1)  # Make sure your environment supports JS rendering
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup

def getnextpage(soup):
    siguiente_tag = soup.find('a', {'aria-label': 'Siguiente'})
    if siguiente_tag and 'href' in siguiente_tag.attrs:
        return base_url + siguiente_tag['href']
    return None

while True:
    print("Fetching data from URL:", url)
    data = getdata(url)

    apartment_listings = []

    listings = data.find_all('div', class_='listing__item')  # Adjusted class to match your HTML structure

    for listing in listings:
        listing_html = str(listing)
        listing_data = {}

        # Extracting the listing URL
        link_tag = listing.find('a', href=True)  # Find the <a> tag with an href attribute
        if link_tag and 'href' in link_tag.attrs:
            listing_data['listing_url'] = base_url + link_tag['href']  # Concatenate base URL with the relative URL
        else:
            listing_data['listing_url'] = 'N/A'  # In case there's no link

        for key, pattern in patterns.items():
            match = re.search(pattern, listing_html)
            listing_data[key] = match.group(1).replace('.', '') if match else 'N/A'

        price_text = listing.find('p', class_='card__price').get_text(strip=True)
        if "consultar precio" in price_text.lower():
            listing_data['price'] = 'Consultar Precio'
        else:
            price_match = re.search(r'\$\s*([\d\.]+)(?!\s*expensas)', price_text)
            listing_data['price'] = price_match.group(1).replace('.', '') if price_match else 'N/A'
        listing_data['url'] = url  # Added 'url' to the data being captured

        apartment_listings.append(listing_data)

    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        for listing in apartment_listings:
            writer.writerow(listing)

    sleep_duration = random.uniform(0.1, 1)
    time.sleep(sleep_duration)

    next_page_url = getnextpage(data)
    if not next_page_url:
        break
    url = next_page_url
