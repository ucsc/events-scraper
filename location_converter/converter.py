import requests
import json

def convert_address_components(address_components):
    """
    converts address components dictionary from google reverse geocoding results
    :param address_components:
    :return:
    """
    return_dict = {}
    valid_components = {
        'street_number',
        'route',
        'locality',
        'administrative_area_level_1',
        'country',
        'postal_code'
    }

    for component in address_components:
        for type in component['types']:
            if type in valid_components:
                return_dict[type] = component['long_name']

    return return_dict

csv_filename = 'locations.csv'

api_key = 'AIzaSyCHuPLkBcYjp9vLmV31Rhv15re0fxK0jUM'

reverse_geo_url = 'https://maps.googleapis.com/maps/api/geocode/json'

column_titles = [
        'Name',
        'Description',
        'Type',
        'URL',
        'Address',
        'City',
        'State',
        'Zip',
        'Phone',
        'Photo URL',
        'Directions',
        'Parking',
        'Hours',
        'Twitter',
        'Facebook URL'
    ]

location_dict = json.loads(open('locations.json').read())

location_list = location_dict['locations']

export_file = open(csv_filename, 'w')

for header in column_titles:
    export_file.write(str(header) + ',')

export_file.write('\n')

for location_subdict in location_list:
    location = location_subdict['location']
    title = ''
    street_address = ''
    city = ''
    state = ''
    postal_code = ''

    if 'title' in location:
        title = location['title']

    if 'street_address' in location:
        street_address = location['street_address']

    if 'city' in location:
        city = location['city']

    if 'state' in location:
        state = location['state']

    if 'postal_code' in location:
        postal_code = location['postal_code']

    if not (len(street_address) > 0 and
                    len(city) > 0 and
                    len(state) > 0 and
                    len(postal_code) > 0):
        payload = {'latlng': location['geo'], 'key': api_key}
        response = requests.get(reverse_geo_url, params=payload)
        geo_dict = response.json()
        geo_results = geo_dict['results']
        geo_entry = geo_results[0]
        address_components = convert_address_components(geo_entry['address_components'])

        street_address = address_components['street_number'] + ' ' + address_components['route']
        city = address_components['locality']
        state = address_components['administrative_area_level_1']
        postal_code = address_components['postal_code']

    address_dict = {
        'Name': title,
        'Address': street_address,
        'City': city,
        'State': state,
        'Zip': postal_code
    }




