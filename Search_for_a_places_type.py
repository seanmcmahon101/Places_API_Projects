import googlemaps

def fetch_place_types(api_key, place_name):
    gmaps = googlemaps.Client(key=api_key)
    search_result = gmaps.places(query=place_name)
    
    if search_result['results']:
        place_id = search_result['results'][0]['place_id']
        details = gmaps.place(place_id=place_id)['result']
        types = details.get('types', [])
        return types
    else:
        return None

api_key = 'AIzaSyD3tmKgmmqwD2LMba87OeVe2oLcR7NLzNU'  # Replace with your actual API key
place_name = 'Java Roastery'
types = fetch_place_types(api_key, place_name)

if types is not None:
    print(f"The types of '{place_name}' are: {', '.join(types)}")
else:
    print(f"No place found with the name '{place_name}'")