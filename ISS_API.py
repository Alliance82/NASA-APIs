# Created By Alliance82
# Created On 01/02/2024
# This program calls the ISS API and returns the location of the international space station
import sqlite3
import json, urllib.request, time, datetime as DT
import numpy as np
import pandas as pd
import sys
import os

# International Space Station (ISS) URL
url = "http://api.open-notify.org/iss-now.json"
# ISS data is updated every 5 seconds, this is to pause the loop to ping in every 5 seconds 
# and measure how much time has passed
interval = 5 
duration = .5 * 60 
start_time = time.time()
iss_loc = []
while time.time() - start_time < duration:
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    time.sleep(interval)
    iss_loc.append(data)
    
df = pd.DataFrame(iss_loc)
print(df)