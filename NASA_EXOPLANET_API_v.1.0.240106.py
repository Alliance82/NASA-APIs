# Created By Alliance82
# Created On 1/6/2024
# Connects To NASA's Exoplanet API Database
# This API uses combines the concept of API querying with SQL Queries
# The Exoplanet Archive uses familiar SQL terms in building the queries
import json, urllib.request, time, datetime as DT
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import urllib.parse

# Base url and format of data to be returned
burl = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query="
format = "&format=json"
# List of fields to build url for the API Query
return_columns = [
    'pl_name',
    'hostname',
    'gaia_id',
    'disc_year'
]
table = "ps"
#query_filters="+where+pl_name+like+%27%25Her%25%27+order+by+pl_orbper+desc"
query_filters="+order+by+pl_orbper+desc"
query = "select+" + (','.join(return_columns)) + "+from+" + table+"+" + query_filters
furl = burl+query+format
print(furl)
response = urllib.request.urlopen(furl)
print(response)
data = json.loads(response.read())
print(data)

# Extract 'pl_name' and 'disc_year' from each entry
planet_names = np.array([entry['pl_name'] for entry in data])
disc_years = np.array([entry['disc_year'] for entry in data])

# Get unique discovery years so that the years can be used for counts and then can be plotted
unique_years = np.unique(disc_years)

# The data contains some of the same planets multiple times, so unique counts are performed
planets_discovered = [np.unique(planet_names[disc_years == year]).size for year in unique_years]

# Trying to Add (0, 0) to the data to force a trendline to start at the origin
# unique_years = [0] + unique_years.tolist()
# planets_discovered = [0] + planets_discovered

plt.scatter(unique_years, planets_discovered, marker='o', color='blue')
plt.xlabel('Years')
plt.ylabel('Planets Discovered')
plt.title('Count of Planet Names by Discovery Year')
plt.grid(True)
plt.show()
