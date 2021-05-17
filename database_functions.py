import mariadb
import configparser

''' MySQL Database : ------------------------------------------------------------ '''
'''                  | post_id | shp_owner | latitude | longtitude | excel_copy | '''
'''                  ------------------------------------------------------------ '''
''' https://mariadb.com/docs/clients/connector-python/                            '''

def connectDB():
    config = configparser.ConfigParser()
    #config.read('config/config.ini')
    config.read('/root/my_python_scripts/config/config.ini')    
    # Instantiate Connection
    try:
        conn = mariadb.connect(
            user=config['Settings']['user'],
            password=config['Settings']['password'],
            host=config['Settings']['host'],
            port=int(config['Settings']['port']),
            database=config['Settings']['database'])
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        exit(0)
    return (conn)

def setDB(conn, ship_id, longitude, latitude, speed, last_auto_update):
    # Insert Data
    cursor = conn.cursor()

    try: 
        if longitude == 0:  # Mode: Update just 1 field
            cursor.execute("UPDATE iR4muqNI_acf_ships SET last_auto_update = ? WHERE ship_id = ?", (last_auto_update,ship_id)) 
        else:  # Mode: Update all fields
            cursor.execute("UPDATE iR4muqNI_acf_ships SET latitude = ?, longitude = ?, speed = ?, last_auto_update = ? WHERE ship_id = ?", (latitude,longitude,speed,last_auto_update,ship_id)) 
    except mariadb.Error as e: 
        print(f"Error during the Update Query: {e}")
    conn.commit()

    print(f"Database Update was run, Affected Rows: {cursor.rowcount}")

def getDB(conn):
    # Retrieve Data
    cursor = conn.cursor()

    cursor.execute("SELECT ship_id FROM iR4muqNI_acf_ships")

    # Get Result-set
    return (tuple(cursor))

def setDBPastPositions(conn, ship_id, longitude, latitude, timestamp):
    # Append Data
    cursor = conn.cursor()

    position_value = "->"+timestamp+":"+str(latitude)+","+str(longitude)

    try: 
        if longitude != 0:       
            cursor.execute("UPDATE iR4muqNI_acf_ships SET past_positions = concat(ifnull(past_positions,''), ?) WHERE ship_id = ?", (position_value, ship_id)) 
    except mariadb.Error as e: 
        print(f"Error during the Update Query: {e}")
    conn.commit()

    print(f"Past Position Update was run, Affected Rows: {cursor.rowcount}")    