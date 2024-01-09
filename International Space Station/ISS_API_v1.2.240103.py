# Created By Alliance82
# Created On 01/02/2024
# This program calls the ISS API and returns the location of the international space station
import sqlite3
import json, urllib.request, time, datetime as DT
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import matplotlib.image as mpimg
from shapely.geometry import Point
import sys
import os

# International Space Station (ISS) URL
url = "http://api.open-notify.org/iss-now.json"
# Importing the shape file
gdf = gpd.read_file('CNTR_BN_20M_2020_4326.shp')
# ISS data is updated every 5 seconds, this is to pause the loop to ping in every 5 seconds 
# and measure how much time has passed
interval = 1
duration = .1 * 60 
start_time = time.time()
iss_loc = []
while time.time() - start_time < duration:
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    time.sleep(interval)
    iss_loc.append(data)
    
df = pd.DataFrame(iss_loc)
position_df = df['iss_position'].apply(pd.Series)
print(position_df.dtypes)
print(position_df.columns)

lat = position_df.loc[0, 'latitude']
lon = position_df.loc[0, 'longitude']

print(f"The ISS is currently located at longitude {lon} and latitude {lat}.")

# Setting up the scaling and sizing of the image
image_width_in_pixels = 640  
image_height_in_pixels = 480 
scale = .025  

# Centering the image requires adjusting the longitude and latitude by equal amounts
lon = str(float(lon) - image_width_in_pixels * scale)
lat = str(float(lat) - image_height_in_pixels * scale)
lon_end = str(float(lon) + image_width_in_pixels * scale)
lat_end = str(float(lat) + image_height_in_pixels * scale)

# Converting lon, lat to GeoDataFrame geometry
geometry = [Point(lon, lat), Point(lon_end, lat_end)]
geo_series = gpd.GeoSeries(geometry, crs='EPSG:4326')

# Convert the geometry to the GeoDataFrame's CRS
geo_series = geo_series.to_crs(gdf.crs)

# Get the transformed coordinates
lon_crs, lat_crs = geo_series.geometry.x[0], geo_series.geometry.y[0]
lon_end, lat_end = geo_series.geometry.x[1], geo_series.geometry.y[1]

img = mpimg.imread('international-space-station.png')

fig, ax = plt.subplots()

# Plot the GeoDataFrame with customized line color and width
gdf.plot(ax=ax, color='black', linewidth=0.5)
ax.set_xlim([-180, 180])
ax.set_ylim([-90, 90])
ax.set_xticks(np.arange(-180, 181, 30))
ax.set_yticks(np.arange(-90, 91, 15))
ax.imshow(img, extent=[lon_crs, lon_end, lat_crs, lat_end], alpha=1, aspect='auto')
ax.set_aspect('equal')
plt.show()
