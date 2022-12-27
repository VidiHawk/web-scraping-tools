''' <!--- BEWARE OF GOOGLE PLACE API COST ---!>
- Nearby search starts at 0.032 USD per request (32.00 USD per 1000)
- Place Details starts at 0.017 USD per request (17.00 USD per 1000)
- Photos downloads starts at 0.007 USD per request (7.00 USD per 1000)

This code takes a geojson file as input and follows the following steps:
- get_place_ids() iterates through json input file and get the coordinates of each place,
then locates a relevant power plant nearby via the Place API.
- get_photo_urls() fetches 5 image urls for each place with the Place Details API.
- get_photos() downloads each image from the Place Photo API.
'''

import json
import requests
from dotenv import load_dotenv # pip3 install python-dotenv
import os

load_dotenv()
token = os.environ.get("GMAP_TOKEN")


def get_place_ids(max_cost):
    cost = 0
    data_json = json.load(open(in_file))
    unsuccessful_retrieves = 0
    for i in data_json["features"]:
        if "place_id" not in i["properties"]:
            coordinates = i["geometry"]["coordinates"]
            lng = coordinates[0]
            lat = coordinates[1]
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=1000&key=" + token
            response = requests.get(url).json()
            if response and response.get("status") == "REQUEST_DENIED":
                print(response)
                continue
            elif response and response.get("status") != "ZERO_RESULTS":
                print(json.dumps(response, indent=4, sort_keys=True))
                print('origin name: ', f'{i["properties"]["name"]}, coordinates: {lat}, {lng}')
                print("Number of results: ", len(response["results"]))
                for j in response["results"]:
                    for keyword in keywords:
                        if keyword.lower() in j['name'].lower(): 
                            print("Relevant place: ", j['name'])
                            print("id: ", j['place_id'])
                            i["properties"]["place_name"] = j["name"]
                            i["properties"]["place_id"] = j["place_id"]
                        else:
                            if i["properties"].get("place_id"):
                                continue
                            else:
                                i["properties"]["place_id"] = None
                if i["properties"]["place_id"] == None:
                    print("NO RELEVANT RESULT\n")  
                    unsuccessful_retrieves += 1                 
            else:
                print("url response has no result")
            cost += 0.032
            print("cost: $", cost)
            # input("Press Enter to continue...")
            if cost > max_cost:
                print("MAX COST REACHED! You already spent $", cost)
                input("Press Enter to continue, or CTRL + C to abort")
        else:
            pass
    destination = open(out_file, "w")
    json.dump(data_json, destination, indent = 4, sort_keys=True)
    destination.close()
    ratio_ids_retrieved = (len(data_json["features"]) - unsuccessful_retrieves)/len((data_json["features"]))
    average_cost = cost / (len(data_json["features"]) * ratio_ids_retrieved)
    print(f"{int(ratio_ids_retrieved/100)}% of ids retrieved. Average cost of ${average_cost} per id retrieved.")


def get_photo_urls(max_cost):
    data_json = json.load(open(in_file))
    cost = 0
    photos = 0
    for i in data_json["features"]:
        if "photo_reference_1" in i["properties"]:
            continue
        else:
            place_id = i["properties"]["place_id"]
            url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name%2Cphoto&key={token}"
            response = requests.get(url).json()
            if response and response.get("status") == "REQUEST_DENIED":
                print(response)
            if response and response.get("status") == "INVALID_REQUEST":
                print(response)
            elif response and response.get("status") != "ZERO_RESULTS":
                print(json.dumps(response, indent=4, sort_keys=True))
                dumped = json.dumps(response)
                place_details = json.loads(dumped)
                a = 0
                if "photos" in place_details['result']:
                    for j in place_details['result']['photos']:
                        photo_reference = j['photo_reference']
                        a += 1
                        photos += 1
                        i["properties"][f"photo_reference_{a}"] = photo_reference
                        if a > 4:
                            print("5 photos added")
                            break
                    cost += 0.017
                    print("cost: $", cost)
                    # input("Press Enter to continue...")
                    if cost > max_cost:
                        print("MAX COST REACHED! You already spent $", cost)
                        input("Press Enter to continue, or CTRL + C to abort")
                else:
                    pass
            else:
                print("No result from place details api for ", i["properties"]["name"])
    destination = open(out_file, "w")
    json.dump(data_json, destination, indent = 4, sort_keys=True)
    destination.close()
    nb_places = len(data_json["features"])
    print(f"A total of {photos} photos were retrieved for {nb_places} places. Average cost of ${nb_places*0.017/photos} per photo retrieved.")


def get_photos(max_cost):
    data_json = json.load(open(in_file))
    cost = 0
    photos_saved = 0
    a = 0
    for i in data_json["features"]:
        a += 1
        if f"photo_reference_{a}" in i["properties"]:
            photo_ref = i["properties"][f"photo_reference_{a}"]
            url = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=752&photo_reference={photo_ref}&key={token}'
            response = requests.get(url)
            img_destination = "data/googlemap_places/photos/" + i["properties"]["id"] + f"_{a}" + ".png"
            fp = open(img_destination, "wb")
            fp.write(response.content) 
            fp.close()
            photos_saved += 1
            cost += 0.07
            print(f"Cost: ${cost}")
            input("Press Enter to continue...")
            if cost > max_cost:
                print("MAX COST REACHED! You already spent $", cost)
                input("Press Enter to continue, or CTRL + C to abort")
        else:
            name = i["properties"]["name"]
            a = 0
            print(f"{a} photos saved for {name}.")
    print(f"A total of {photos_saved} photos were saved.")
        
    
in_file = 'data/googlemap_places/in.geojson'
out_file = "data/googlemap_places/out.geojson"
keywords = ["Wind", "Hydro", "Coal", "Gas", "Nuclear", "Solar", "power", "plant", 'station']
max_cost = 2 # in USD


# get_place_ids(max_cost)
# get_photo_urls(max_cost)
get_photos(max_cost)






