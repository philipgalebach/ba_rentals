#zonaprop working html

from bs4 import BeautifulSoup
import csv

# Function to extract data from each listing
def extract_data(soup):
    data = []
    listings = soup.find_all('div', attrs={"data-qa": "posting PROPERTY"})
    for listing in listings:
        price_div = listing.find('div', attrs={"data-qa": "POSTING_CARD_PRICE"})
        price = price_div.text.strip() if price_div else "Consultar Precio"

        expenses_div = listing.find('div', attrs={"data-qa": "expensas"})
        # Extract the full value of expenses
        expenses = expenses_div.text.replace('Expensas', '').strip() if expenses_div else ""

        address_div = listing.find('div', class_="sc-ge2uzh-0 hUCXbI")
        address = address_div.text.strip() if address_div else ""

        size_span = listing.find('span', text=lambda t: t and 'm²' in t)
        size = size_span.text.strip() if size_span else ""

        bedrooms_span = listing.find('span', text=lambda t: t and 'dorm.' in t)
        bedrooms = bedrooms_span.text.strip() if bedrooms_span else ""

        bathrooms_span = listing.find('span', text=lambda t: t and 'baños' in t)
        bathrooms = bathrooms_span.text.strip() if bathrooms_span else ""

        url = ""

        # Correctly extract the listing URL using the 'data-to-posting' attribute from the correct div
        listing_url = "https://www.zonaprop.com.ar" + listing.get('data-to-posting', '') if listing else ""

        data.append([price, expenses, address, size, bedrooms, bathrooms, url, listing_url])
    return data

# Load the HTML content from a file
file_path = '/path/to/your/html/file.html'
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract data using the function
apartment_data = extract_data(soup)

# Define the CSV file path and headers
csv_file_path = '/path/to/your/output/apartment_listings.csv'
headers = ["Price", "Expenses", "Address", "Size", "Bedrooms", "Bathrooms", "URL", "Listing URL"]

# Write the data to the CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Write the header
    writer.writerows(apartment_data)  # Write the data

print(f"Data successfully written to {csv_file_path}")
