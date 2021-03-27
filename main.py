import database_functions
from marinetrafficapi import MarineTrafficApi
from marinetrafficapi import exceptions
from datetime import datetime

# Connect to DB
#conn = database_functions.connectDB()
# Get ship names from DB
#database_functions.getDB(conn) 

testname1 = "hello"

# Connect to the API
api = MarineTrafficApi(api_key="56d7d3f632a4565405a7ed674ff5165ef830a31b")
# Query the API (https://www.marinetraffic.com/en/ais-api-services/documentation/api-service:ps07)
try:
    vessel = api.single_vessel_positions(time_span=20,
                                        msg_type='simple',
                                        mmsi=370272000)
    MarineTrafficApi.print_params_for('single_vessel_positions')
    vessel = vessel.models[0]

    longitude = vessel.longitude.value
    latitude = vessel.latitude.value
    last_auto_update = "Coordinate timestamp is " + str(vessel.timestamp.value) + " UTC"

except exceptions.MarineTrafficRequestApiException as e:
    print(f"API Request Error: {e}")
    time_now_utc = datetime.utcnow().replace(microsecond=0)

    longitude = 0
    latitude = 0
    last_auto_update = "Attempted at " + str(time_now_utc) + " UTC, but failed"

print(longitude, latitude, last_auto_update)

# Update DB
#database_functions.setDB(conn)