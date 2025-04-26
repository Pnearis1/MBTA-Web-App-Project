import os
import json
import urllib.request
import pprint

from urllib.parse import quote
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys from environment variables
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

# Useful base URLs (you need to add the appropriate parameters for each API request)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"


def get_coordinates(place_name):
    """Takes a place name and returns (latitude, longitude) tuple"""
    encoded_place = urllib.parse.quote(place_name)
    url = f"{MAPBOX_BASE_URL}/{encoded_place}.json?access_token={MAPBOX_TOKEN}&types=poi"

    with urllib.request.urlopen(url) as response:
        data = json.load(response)
        coords = data["features"][0]["center"]
        return coords[1], coords[0]  # lat, lon
    
def get_json(url: str) -> dict: #this code is used to get the json data from the url
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode("utf-8"))

def get_lat_lng(place_name: str) -> tuple[str, str]: #this code is used to get the letitude and longitude of the place
    query = quote(place_name)
    url = f"{MAPBOX_BASE_URL}/{query}.json?access_token={MAPBOX_TOKEN}&types=address,place,poi"
    data = get_json(url)
    coordinates = data["features"][0]["geometry"]["coordinates"]
    return str(coordinates[1]), str(coordinates[0])

def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
#Takes coordinates and returns (station_name, wheelchair_accessible)
    url = (
        f"https://api-v3.mbta.com/stops?api_key={MBTA_API_KEY}"
        f"&filter[latitude]={latitude}&filter[longitude]={longitude}&sort=distance"
    )

    with urllib.request.urlopen(url) as response:
        data = json.load(response)
        stop = data["data"][0]["attributes"]
        return stop["name"], stop["wheelchair_boarding"] == 1
def find_stop_near(place_name: str) -> tuple[str, bool]: #this code is used to find the nearest stop near the place name
    lat, lon = get_coordinates(place_name)
    return get_nearest_station(lat, lon)

def main(): # Example usage
    place = "Boston Public Library"
    lat, lng = get_lat_lng(place)
    print(f"Coordinates of {place}: {lat}, {lng}")
    stop, accessible = get_nearest_station(lat, lng)
    print(f"Nearest Stop: {stop}, Accessible: {'Yes' if accessible else  'No'}")

# Example usage of find_stop_near function
if __name__ == "__main__":
    main()
