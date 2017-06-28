import pandas as pd
import numpy as np

#load a file containing a list of postcodes, latitudes and longitudes - 
#the locations for which the drive time is required
postcodes = pd.read_csv('filename.csv', sep = ',', encoding = "ISO-8859-1", header = 0)
cols_to_use = ['Postcode', 'lat','lon']
postcodes = postcodes[cols_to_use]

#%% loop to create a half a matrix of drive times

#form an empty matrix
driveTime = np.empty([len(postcodes), len(postcodes)])

import urllib.request
import json as simplejson

count = 0
for location1 in range(len(postcodes)):
    count = count+1
    for location2 in range(location1+1, len(postcodes)):
        
        orig_lat = postcodes.iloc[location1][1]
        orig_lon = postcodes.iloc[location1][2]
        
        dest_lat = postcodes.iloc[location2][1]
        dest_lon = postcodes.iloc[location2][2]
        
        url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins=%1.7f,%1.7f&destinations=%1.7f,%1.7f&mode=driving&language=en-EN&sensor=false" % (orig_lat,orig_lon, dest_lat, dest_lon)
        result = urllib.request.urlopen(url)
        str_result = result.read().decode('utf-8')
        obj = simplejson.loads(str_result)
        #populate the numpy matrix with drive time in seconds
        driveTime[location1, location2] = obj['rows'][0]['elements'][0]['duration']['value']

driveTimeDF = pd.DataFrame(driveTime) 

#copy the upper triangle into the lower
num_rows = np.size(driveTime,0)
num_cols = np.size(driveTime,1)
           
for i in range(num_rows):
    for j in range(i, num_cols):
        driveTime[j][i] = driveTime[i][j]


#add a column and a row with original postcodes
postcode = postcodes['Postcode']
driveTimeDF_full = pd.DataFrame(driveTime, columns = postcode)

#save to csv
driveTimeDF_full.to_csv('driveTimeDF_full.csv', index = False, sep=',',header=True)
