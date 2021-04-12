import database_functions
import configparser
from marinetrafficapi import MarineTrafficApi
from marinetrafficapi import exceptions
from datetime import datetime

# Config Parsing
config = configparser.ConfigParser()
config.read('config/config.ini')
#config.read('/root/my_python_scripts/config/config.ini')

# Connect to DB
conn = database_functions.connectDB()
# Get ship IDs from DB
ship_ids = database_functions.getDB(conn) 

# Connect to the API
api = MarineTrafficApi(api_key=config['API']['api_key'])
# Query the API (https://www.marinetraffic.com/en/ais-api-services/documentation/api-service:ps07)
MarineTrafficApi.print_params_for('single_vessel_positions')
count_used_credits = int(config['API']['used_credits'])
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

config.set('API', 'used_credits', str(count_used_credits))
with open('config/config.ini', 'w') as configfile:
#with open('/root/my_python_scripts/config/config.ini', 'w') as configfile:
    config.write(configfile)

conn.close()