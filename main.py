import database_functions

# Connect to DB
conn = database_functions.connectDB()
# Get ship names from DB
database_functions.getDB(conn) 

testname1 = "hello"