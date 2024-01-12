import os
import csv
import random
import time
from requests_html import HTMLSession
from bs4 import BeautifulSoup

# Define the website info
csv_file_path = './zonaprop_listings.csv'
base_url = 'https://www.zonaprop.com.ar'
page_url = base_url + '/departamentos-alquiler-capital-federal-mas-de-3-habitaciones-a-estrenar-pagina-2.html?utm_source=google&utm_medium=cpc&utm_campaign=Search_Sale_CABA_Tipo-inmueble_DSA&utm_content=Departamentos&utm_term=&gad_source=1&gclid=Cj0KCQiA1rSsBhDHARIsANB4EJYfWC1IN97GXZZ7axVfkqBqWhT92HBkM8zU2yN-k9rj-zZFMaQcfzcaAiP_EALw_wcB'
headers = ['website', 'price', 'expenses', 'address', 'size', 'bedrooms', 'bathrooms', 'url', 'listing_url']

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# If you're on macOS or Linux:

chrome_driver_path = '/Users/philip.galebach/path/to/chromedriver'  # Update this line


# Set up Selenium with headless Chrome
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")  # Adjust as needed
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)



# Replace with the actual URL you want to scrape
url = page_url

# Navigate to the page
driver.get(url)

# Wait for the page to load. Adjust the time as necessary.
time.sleep(1)  # Waits for 5 seconds

# Once the page is loaded, get the page source
page_source = driver.page_source

# Use BeautifulSoup to parse the page source
soup = BeautifulSoup(page_source, 'html.parser')

print(soup)

# Attempt to find elements by class name. Update this with the correct class.
# properties = soup.find_all('div', class_='postingCard')

# # Close the browser
# driver.quit()

# print(properties)




# Create a session object
# s = HTMLSession()

# try:
#     print(page_url)
#     # Make a request to the website
#     page_response = s.get(page_url)
#     # Parse the content with BeautifulSoup
#     page_content = BeautifulSoup(page_response.content, 'lxml')  # or 'html.parser'
#     print(page_content)
#     # Find all property elements
#     properties = page_content.find_all('div', class_='postingCard')
#     print(properties)

# except Exception as e:
#     print(f"An error occurred: {e}")
