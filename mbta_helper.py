from typing import Mapping
import config
import urllib.request
import json
import pprint



# Useful URLs (you need to add the appropriate parameters for your requests)
MAPQUEST_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"


# Your API KEYS (you need to use your own keys - very long random characters)
MAPQUEST_API_KEY = config.MapQuest_consumer_key
MBTA_API_KEY = config.MTBA_key
MAPQUEST_URL = f'http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&location=Boston,MA'

# A little bit of scaffolding if you want to use it

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding  API URL formatting requirements.
    """
    MAPQUEST_URL = f'http://www.mapquestapi.com/geocoding/v1/address?&key={MAPQUEST_API_KEY}&location={place_name}'
    MAPQUEST_INFO = get_json(MAPQUEST_URL)
    # pprint.pprint(MAPQUEST_INFO)
    LAT_LONG = MAPQUEST_INFO['results'][0]['locations'][0]['latLng']
    LAT = LAT_LONG['lat']
    LONG = LAT_LONG['lng']
    return [LAT , LONG]




def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible)
    tuple for the nearest MBTA station to the given coordinates.
    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL
    formatting requirements for the 'GET /stops' API.
    """
    sorted_distance_url = f"https://api-v3.mbta.com/stops?api_key={MBTA_API_KEY}&sort=distance&filter%5Blatitude%5D={latitude}&filter%5Blongitude%5D={longitude}"
    f = urllib.request.urlopen(sorted_distance_url)
    print(sorted_distance_url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    print(latitude, longitude)
    # print(response_data)
    is_wheelchair = response_data['data'][0]['attributes']['wheelchair_boarding']
    if is_wheelchair == 0:
        wheelchair_accessible = 'No Wheelchair Information'
    elif is_wheelchair == 1:
        wheelchair_accessible = 'Wheelchair Accessible'
    else:
        wheelchair_accessible = 'Wheelchair Inaccessable'
    return (response_data['data'][0]['attributes']['name'], wheelchair_accessible)


def find_stop_near(place_name):
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
    """
    lat_long = get_lat_long(place_name)
    return get_nearest_station(lat_long[0], lat_long[1])


def main():
    """"
    You can test all the functions here
    """
    # pprint.pprint(get_json(MAPQUEST_URL))
    # pprint.pprint(get_json(MBTA_BASE_URL))
    # print(get_lat_long('VassarSt,Cambridge,MA'))
    # print(get_nearest_station(42.365248, -71.105015))


if __name__ == '__main__':
    main()
