# Created by Alliance82
# Created on 9/8/2021
# This pulls in NASA data for any known near-Earth asteroids and whether they pose a threat to Earth
import json
import urllib.request
import time

today = time.strftime('%Y-%m-%d', time.gmtime())
apiKey = ""
print("Date: " + today)

#Our JSON request to retrieve data about asteroids approaching planet Earth.
url = "https://api.nasa.gov/neo/rest/v1/feed?start_date=" + today + "&end_date=" + today + "&api_key="+apiKey

response = urllib.request.urlopen(url)
result = json.loads(response.read())

print("Today " + str(result["element_count"]) + " asteroids will be passing close to planet Earth:")
print("")
asteroids = result["near_earth_objects"]

# Parsing all the JSON data:
for x in asteroids:
    for field in asteroids[x]:
      try:
        print(x)
        print("Asteroid Name: " + field["name"])
        #print("Estimated Diameter: " + str(round((field["estimated_diameter"]["meters"]["estimated_diameter_min"]+field["estimated_diameter"]["meters"]["estimated_diameter_max"])/2),0) + " meters")
        #print("Close Approach Date & Time: " + field["close_approach_data"][0]["close_approach_date_full"])
        print("Velocity: " + str(field["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"]) + " km/h") 
        print("Distance to Earth: " + str(field["close_approach_data"][0]["miss_distance"]["kilometers"]) + " km") 
   
        if field["is_potentially_hazardous_asteroid"]:   
          print ("This asteroid could be dangerous to planet Earth!")
        else:
          print ("This asteroid poses no threat to planet Earth!")
      except:
        print("Unable to access all data.")  
      print("--------------------")