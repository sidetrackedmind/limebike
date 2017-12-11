import sys, os
import requests
import geojson
from geojson import Feature, Point, FeatureCollection
from time import sleep


def _location_query(user_lat, user_long):
    #base URL for limebike API
    baseurl = 'https://web-production.lime.bike/api/public/v1/views/bikes?'
    #formatted query based on LimeBike API
    query = 'map_center_latitude={0}&map_center_longitude={1}&user_latitude={0}&user_longitude={1}'.format(user_lat, user_long)
    try:
        r = requests.get((baseurl + query))
        #print(r.url)
        return r.json()
    except:
        print('error')

def create_feature_collection(user_lat_long_list):
    '''Input - list of latitude and longitude tuples [(user_latitude, user_longitude)]
        Output - geojson feature collection
        This function will call the LimeBike API and return information
        for the 50 closest bikes. This function will turn that API text
        into a geojson with the following features:
        - Points with latitude and longitude
        - Properties: bike_id (1-50 based on the request - not unique)
                    last_activity_at date
    '''
    location_geojson_list = []
    feature_list = []
    for lat_long in user_lat_long_list:
        location_geojson = _location_query(lat_long[0],lat_long[1])
        location_geojson_list.append(location_geojson)
    for location_geojson in location_geojson_list:
        for bikes in location_geojson['data']['attributes']['nearby_locked_bikes']:
            us_lat = bikes['attributes']['latitude']
            us_long = bikes['attributes']['longitude']
            bike_id = bikes['id']
            last_activity = bikes['attributes']['last_activity_at']
            my_feature = Feature(geometry=Point((us_long,us_lat)), properties={"bike_id": bike_id, "last_activity_at": last_activity})
            feature_list.append(my_feature)
    feature_collection = FeatureCollection(feature_list)
    return feature_collection

def output_geojson(filename, feature_collection):
    '''Input - filename and feature_collection
        Output - geojson file called 'filename'
     '''
    with open(filename, 'w') as outfile:
        geojson.dump(feature_collection, outfile)

def append_feature_collection(filename,new_feature):
    '''import json
    # Load existing data
    with open('test.json') as f:
      data = json.load(f)
    # Add data
    feature = {}
    feature['type'] = 'Feature'
    feature['geometry'] = {'type': 'Point',
                           'coordinates': [10, 10],
                           }
    feature['properties'] =  {'prop0': 'value1'}
    data['features'].append(feature)

    # Write JSON file with new data
    with open('test.json', 'w') as f:
      f.write(json.dumps(data))
    '''
    pass
