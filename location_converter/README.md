# Location Converter
Converts a JSON feed containing UCSC places to CSV

Translates the coordinates of any places that don't have an address, into addresses using the google maps reverse geocoding API


## To run

make sure you have the virtualenv created and activated, and the locations.json file is in the same folder as this script

    python3 converter.py

will output the locations.csv file