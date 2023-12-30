import googlemaps
import pandas as pd
import csv
import time
import math

def fetch_coffee_shops(api_key, location, radius=1000):
    gmaps = googlemaps.Client(key=api_key)
    coffee_shops = []
    type_ = 'cafe'  # Specify the type as 'cafe'

    # Nearby places search
    page_token = None
    while True:
        places_result = gmaps.places_nearby(location=location, radius=radius, type=type_, page_token=page_token)
        for place in places_result['results']:
            details = gmaps.place(place_id=place['place_id'])['result']
            name = details.get('name')
            rating = details.get('rating', 0)
            reviews = details.get('user_ratings_total', 0)
            coffee_shops.append((name, rating, reviews))

        page_token = places_result.get('next_page_token')
        if not page_token:
            break

        time.sleep(2)  # Ensure enough delay before the next API call

    # Text search query
    query = 'coffee in Birmingham'
    places_result = gmaps.places(query=query)
    for place in places_result['results']:
        details = gmaps.place(place_id=place['place_id'])['result']
        name = details.get('name')
        rating = details.get('rating', 0)
        reviews = details.get('user_ratings_total', 0)
        coffee_shops.append((name, rating, reviews))

    # Remove duplicates
    coffee_shops = list(set(coffee_shops))

    # Calculate the score for each coffee shop
    max_reviews = max(coffee_shops, key=lambda x: x[2])[2]  # Get the maximum number of reviews
    for i in range(len(coffee_shops)):
        name, rating, reviews = coffee_shops[i]
        score = rating * (math.log(1 + reviews) / math.log(1 + max_reviews))  # Calculate the score
        coffee_shops[i] = (name, rating, reviews, score)  # Create a new tuple with the score included


    return coffee_shops


def save_to_csv(coffee_shops, filename='test_output_BRUM_MATHTEST2.csv'):  # Changed filename
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Rating', 'Reviews', 'Ratio'])
        writer.writerows(coffee_shops)

api_key = 'AIzaSyD3tmKgmmqwD2LMba87OeVe2oLcR7NLzNU'
excel_file_path = '/Users/seanmcmahon/Downloads/BrumCoffee.xlsx'
cities_df = pd.read_excel(excel_file_path)

# Limiting to first 2 cities for testing
test_cities_df = cities_df.head(1)
test_shops = []

for _, row in test_cities_df.iterrows():
    lat, lng = row['Lat'], row['Long']
    location = f"{lat}, {lng}"
    shops = fetch_coffee_shops(api_key, location)
    test_shops.extend(shops)
    time.sleep(1)  # Rate limit delay

save_to_csv(test_shops)
