import database_functions
import configparser
import requests
from marinetrafficapi import MarineTrafficApi
from marinetrafficapi import exceptions
from datetime import datetime

# Config Parsing
config = configparser.ConfigParser()
#config.read('config/config.ini')
config.read('/root/my_python_scripts/config/config.ini')

''' MarineTraffic API '''
''' Mode #1           '''
def mainMarineTraffic(config):
    # Connect to DB
    conn = database_functions.connectDB()
    # Get ship IDs from DB
    ship_ids = database_functions.getDB(conn) 

    # Connect to the API
    api = MarineTrafficApi(api_key=config['API1']['api_key'])
    # Query the API (https://www.marinetraffic.com/en/ais-api-services/documentation/api-service:ps07)
    MarineTrafficApi.print_params_for('single_vessel_positions')
    count_used_credits = int(config['API1']['used_credits'])
    for ship_id in ship_ids:
        print(f"\nRetrieved ship with ID: {ship_id[0]}, now Querying the API...")  

        try:
            vessel = api.single_vessel_positions(time_span=20,
                                                msg_type='simple',
                                                mmsi=ship_id[0])
            vessel = vessel.models[0]
            print(f"API Run Successfully")

            longitude = vessel.longitude.value
            latitude = vessel.latitude.value
            speed = float(vessel.speed.value)/10
            last_auto_update = "Coordinate timestamp is " + str(vessel.timestamp.value) + " UTC"
            count_used_credits += 1

        except exceptions.MarineTrafficRequestApiException as e:
            print(f"API Request Error: {e}")
            time_now_utc = datetime.utcnow().replace(microsecond=0)

            longitude = 0
            latitude = 0
            speed = 0
            last_auto_update = "Attempted at " + str(time_now_utc) + " UTC, but failed. Vessel not found."

        except IndexError as e:
            print(f"API Request Error, ship exists but position is too old: {e}")
            time_now_utc = datetime.utcnow().replace(microsecond=0)

            longitude = 0
            latitude = 0
            speed = 0        
            last_auto_update = "Attempted at " + str(time_now_utc) + " UTC, but failed. Vessel exists but position is too old"

        # Update DB
        database_functions.setDB(conn, ship_id[0], longitude, latitude, speed, last_auto_update)

    config.set('API1', 'used_credits', str(count_used_credits))
    #with open('config/config.ini', 'w') as configfile:
    with open('/root/my_python_scripts/config/config.ini', 'w') as configfile:
        config.write(configfile)

    conn.close()

''' VesselFinder API '''
''' Mode #2          '''
def mainVesselFinder(config):
    # Connect to DB
    conn = database_functions.connectDB()
    # Get ship IDs from DB
    ship_ids = database_functions.getDB(conn) 
    ship_ids = [int(item[0]) for item in ship_ids]

    # Query the API (https://api.vesselfinder.com/docs/vesselslist.html)
    # No "for" loop needed here, the ship list is already intergrated in the API
    print(f"\nNow Querying the API...")  

    response = requests.get("https://api.vesselfinder.com/vesselslist?userkey=" + config['API2']['api_key'])
    reponse_obj = response.json()

    for ship in reponse_obj: 
        print() 
        if (response.status_code != 200) or (len(reponse_obj) < 2):
            print(f"API Request Error: Response Error")
            time_now_utc = datetime.utcnow().replace(microsecond=0)

            mmsi = 0
            longitude = 0
            latitude = 0
            speed = 0
            last_auto_update = "Attempted at " + str(time_now_utc) + " UTC, but API Request Error."

        else:
            print(f"API Run Successfully")

            try:
                mmsi = ship["AIS"]["MMSI"]
                longitude = ship["AIS"]["LONGITUDE"]
                latitude = ship["AIS"]["LATITUDE"]
                speed = float(ship["AIS"]["SPEED"])
                last_auto_update = "Coordinate timestamp is " + str(ship["AIS"]["TIMESTAMP"])

            except KeyError as e:
                print(f"API Request Error: {e}")
                time_now_utc = datetime.utcnow().replace(microsecond=0)

                mmsi = 0
                longitude = 0
                latitude = 0
                speed = 0
                last_auto_update = "Attempted at " + str(time_now_utc) + " UTC, but failed. Vessel not found."

        print(last_auto_update)

        print("Ship ID is " + str(mmsi))

        # Update DB
        if mmsi == 0:
            raise Exception("Some sort of Error occured, see above.")
        elif mmsi in ship_ids:
            database_functions.setDB(conn, mmsi, longitude, latitude, speed, last_auto_update)
        else:
            raise Exception("Error: Ship position was retrieved from the API, but not found in Database")         
            
    conn.close()


''' Run Main Function depending on Mode '''
mode = config['API']['mode']
if mode == "1":
    mainMarineTraffic(config)
elif mode == "2":         
    mainVesselFinder(config)