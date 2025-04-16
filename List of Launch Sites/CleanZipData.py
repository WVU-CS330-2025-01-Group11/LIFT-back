

#open US.text
# contains all US zip codes and their coordinates in tab delimited format
# example US	99553	Akutan	Alaska	AK	Aleutians East	013			54.143	-165.7854	1
#isolate the zip codes and their coordinates
# and, in json format, write to a new file called US_coordinates.json

import json
import numpy as np

# print working directory
import os
print(os.getcwd())

with open("List of Launch Sites/US.txt", "r") as f:
    lines = f.readlines()
    
    # split each line by tab
    cols = [line.split("\t") for line in lines]
    # isolate the zip codes and their coordinates
    # zip_codes = [{"zip_code": col[1], "latitude": col[9], "longitude": col[10]} for col in cols]

    npzip_codes = np.array([col[1] for col in cols])
    npcoords = np.array([ [col[9], col[10]] for col in cols])
    # convert to float
    npcoords = npcoords.astype(float)
    # convert to int
    npzip_codes = npzip_codes.astype(int)
    # create a numpy array of shape (n, 3) where n is the number of zip codes
    npzip_codes_array = np.array(list(zip(npzip_codes, npcoords[:,0], npcoords[:,1])), dtype=[('zip_code', 'U10'), ('latitude', 'f8'), ('longitude', 'f8')])

#write to a new file called US_coordinates.json
with open("US_coordinates.json", "w") as f:
    # json.dump(zip_codes, f, indent=4)
    # print(f"Successfully wrote {len(zip_codes)} zip codes to US_coordinates.json")
    
    # save as numpy array
    # save as two separate numpy arrays, zips and coords
    np.save("US_zip_codes.npy", npzip_codes)
    np.save("US_coordinates.npy", npcoords)
    # np.save("US_coordinates.npy", npzip_codes_array)
    # print(f"Successfully wrote {len(npzip_codes_array)} zip codes to US_coordinates.npy")

#load the numpy arrays
npzip_codes = np.load("US_zip_codes.npy")
npcoords = np.load("US_coordinates.npy")
# print the shape of the arrays
print(npzip_codes.shape)
print(npcoords.shape)
print(npzip_codes_array.shape)
# print the first 10 zip codes and their coordinates
print(npzip_codes[:10])
