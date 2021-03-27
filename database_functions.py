import mariadb
import configparser

''' MySQL Database : ------------------------------------------------------------ '''
'''                  | post_id | shp_owner | latitude | longtitude | excel_copy | '''
'''                  ------------------------------------------------------------ '''

def connectDB():
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    # Instantiate Connection
    try:
        conn = mariadb.connect(
            user=config['Settings']['user'],
            password=config['Settings']['password'],
            host=config['Settings']['host'],
            port=int(config['Settings']['port']))
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        exit(0)
    return (conn)

def setDB(conn):
    # TEMP CODE
    cnx = mysql.connector.connect(user='root', password='root', database='newsapp')
    cursor = cnx.cursor()
    cursor.execute('SET NAMES utf8mb4')  # Some symbols are in fact UTF8 4 Bit
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection=utf8mb4")
    query = ("INSERT INTO theguardian VALUES (%s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (countVariable, textVariable, titleVariable, authorVariable, categoryVariable, dateVariable, urlVariable))
    cnx.commit()
    
    cursor.close()
    cnx.close()  

def getDB(conn):
    # GET SHIP NAMES FROM DATASET
    print("hello")

print(connectDB())