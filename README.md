# Events Scraper and Locations Converter
Python Script to scrape events from events.ucsc.edu and convert format them for upload to localist.com
Can also generate groups and locations csv files for localist upload

## Installation

### Prerequisites

This script uses python3, so make sure you have it installed

    sudo apt install python3
 
You will need the python 3 version of pip

    sudo apt install python3-pip

Make sure you have virtualenv installed

    pip3 install virtualenv

You will also need the C bindings for the lxml library which have to be installed before pip tries to install lxml in a virtualenv

    sudo apt install libxml2-dev libxslt-dev

### Main installation

Clone the repository

    git clone https://github.com/ucsc/events-scraper.git

After cloning the repository

    cd events-scraper
    virtualenv venv
    . venv/bin/activate
    pip3 install -r requirements.txt

## Managing the virtualenv

Always activate the virtualenv before running the scraper or the locations converter

    . venv/bin/activate

To deactivate the virtualenv and return to your regular python installation

    deactivate

To remove the virtualenv completeley, simply delete the venv folder

    rm -rf venv

(or be safer and delete it using a file explorer)

## To run

### Run the scraper

    python3 scraper.py

The scraped events will be written to

    event_import.csv

### Command line options summary:

    usage: scraper.py [-h] [-s START_INDEX] [-e END_INDEX] [-g]

    optional arguments:
      -h, --help      show this help message and exit
      -s START_INDEX  The starting index for events, inclusive. Default is 0
      -e END_INDEX    The starting index for events, inclusive. Default is 5,000
      -g              If this flag is added, a csv of groups found will be
                      generated


### Scraping a subset of events

Use the command line arguments specified above for start and end indexes.  

For example, to scrape events 3200 through 3350

    python3 scraper.py -s 3200 -e 3350

### Generating a groups csv export

This is an experimental functionality, which takes the groups fields from the events and generates a csv import of groups for localist.  It is currently not reccomended to use this, as the ucsc event categories are standardize, so the resulting groups csv will not contain consistent groups.

    python3 scraper.py -g

## The Locations Converter
This script located in the location_converter folder converts locations from json format to csv for localist input, while also converting longitutde and latitudes to approximate addresses using google's reverse geocoding api.

If the json object for a location contains both a latitute and a longitude, the script will convert them to an address, otherwise it will use a provided address or ignore the location entirely.

### To run

    cd location_converter
    python3 converter.py