import sys 
import json
import requests
from dotenv import load_dotenv # pip3 install python-dotenv
import os

load_dotenv()
token = os.environ.get("GMAP_TOKEN")

lng = -9.5892
lat = 52.3096
in_file = 'data/googlemap_places/in/test.geojson'
destination = "data/googlemap_places/out/test.geojson"
max_api_calls = 10


# data_json = json.load(open(in_file))

# # get all coordinates from origin geojson file:
# api_calls = 1
# for i in data_json["features"]:
#     # get coordinates from source file:
#     coordinates = i["geometry"]["coordinates"]
#     lng = coordinates[0]
#     lat = coordinates[1]

url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=1000&key=" + token

response = requests.get(url).json()

if response and response.get("status") == "REQUEST_DENIED":
    print(response)
    sys.exit(1)
elif response and response.get("status") != "ZERO_RESULTS":
    print(json.dumps(response, indent=4, sort_keys=True))
    print(len(response["results"]))
    print(">>>> PAGE 1")
    for result in response["results"]:
         print("Store name: ", result["name"])

    # if "next_page_token" in response:
    #     print(">>>> PAGE 2")
    #     page2_token = response["next_page_token"]        
    #     url_page_2 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=19.4196301,-99.16895&radius=20000&type=store&pagetoken=" + page2_token + "&key=" + token
    #     print(url_page_2)
    #     response_page_2 = requests.get(url_page_2).json()
    #     print(response_page_2)
    #     for result in response_page_2["results"]:
    #             print("Store name: ", result["name"])
    # else:
    #     print("no next page")
else:
    print("No result")

out_file = open(destination, "w")
json.dump(response, out_file, indent = 4, sort_keys=True)
out_file.close()