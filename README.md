# Marine Tracking Tool

A tool that tracks Ships/Ports and stores them on an Interactive Map. Supports the two most popular Vessel Tracking Services.

#### `Mode 1: MarineTraffic.com API`

``` python
''' MarineTraffic API '''
''' Mode #1           '''
def mainMarineTraffic(config):
    ...
```

#### `Mode 2: VesselFinder.com API`

``` python
''' VesselFinder API '''
''' Mode #2          '''
def mainVesselFinder(config):
    ...
```

## Running the Tool

1. Install the required Python packages/dependencies.
2. Set the appropriate configuration parameters, since information is stored on a MySQL **Database**. This is done by creating `/config/config.ini` using the following format:

``` ini
[Settings]
host = localhost
port = 3306
user = xxx
password = xxx
database = xxx

[API]
mode = 2
last_execution = 2021-05-13 00:45:22.484915

[API1]
api_key = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
used_credits = xx

[API2]
api_key = XX-XXXXXXXX-XXXXXX
```

3. Run the Python script:

``` bash
python main.py
```

## Features

* Vessel Position Tracking
* Vessel Speed Tracking
* Log Messages depending on Success/Failure
* Log of Past Positions
* [TODO] Port Weather Tracking

## Final System Implementation

<img src="https://github.com/spykard/Marine-Traffic-API/blob/main/screenshots/Map-Overview.png?raw=true" alt="Final System Implementation">

<!-- <p align="center">
  <img src="https://github.com/spykard/Marine-Traffic-API/blob/main/screenshots/Map-Overview.png?raw=true" height="400px" alt="Final System Implementation">
</p> -->