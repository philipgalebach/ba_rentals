import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from datetime import datetime
import logging
import time

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Calculate 'price_total'
dollarblue = 1000  #PJG update to the current rate. 

# today = datetime.now().strftime("%Y-%m-%d")
output_file_path = f'listings_clean.csv'

# Load the CSV data into a DataFrame
df = pd.read_csv('argenprop/argenprop_listings.csv')

# limit to the first comma to remove floors/unit numbers before giving to GSP function
df['address'] = df['address'].apply(lambda x: x.strip().split(',')[0] + ', CABA, Argentina')

geolocator = Nominatim(user_agent="geoapiExercises")

def get_long_lat(address):
    try:
        time.sleep(1)  # Delay to prevent rate limiting
        location = geolocator.geocode(address)
        if location:
            return location.longitude, location.latitude
        else:
            logger.warning(f"Could not geocode address: {address}")
            return None, None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        logger.error(f"Geocoding error for address {address}: {e}")
        return None, None

# Deduplicate listings based on the address, using first timestamp it was added to my data. 
df = df.assign(timestamp=pd.to_datetime(df['timestamp'])).sort_values('timestamp').drop_duplicates('address', keep='first')

df['price_total_usd'] = df.apply(lambda row: (row['price'] / dollarblue + row['expenses'] / dollarblue) if row['currency'] == '$' 
                             else (row['price'] + row['expenses']/ dollarblue), axis=1)

# Apply the function to create longitude and latitude fields
# df['longitude'], df['latitude'] = zip(*df['address'].map(get_long_lat))

filtered_df = df[
    (df['size'].isna() | (df['size'] >= 90)) & 
    (df['price_total_usd'] <= 1500) & 
    (df['price_total_usd'] >= 300) & 
    df['price_total_usd'].notna() & 
    (df['timestamp'].dt.date == pd.Timestamp(datetime.now().strftime("%Y-%m-%d")).date())
]
# 5. Export to a new CSV file
filtered_df.to_csv(output_file_path, index=False)

print(f"File saved as {output_file_path}")
