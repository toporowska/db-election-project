import getpass
import psycopg2

#establishing the connection
user = input("Username: ")
password = getpass.getpass("Password: ")

conn = psycopg2.connect(
   database="postgres", user=user, password=password, host='127.0.0.1', port= '5432'
)
conn.autocommit = True

#Creating a cursor
cursor = conn.cursor()

#Preparing query to create a database and creating database
# COMMENT NEXT TWO LINES OUT WHEN RUNNING THIS FOR THE N-TH TIME (when N > 1)
sql = '''CREATE database election''';
cursor.execute(sql)

conn = psycopg2.connect(
   database="election", user=user, password=password, host='127.0.0.1', port= '5432'
)
conn.autocommit = True

#Creating a cursor object connected to the election database
cursor = conn.cursor()

#Clearing existing tables and functions (in case it's not the first time this runs)
reader = open("clear.sql","r")
query = reader.read()
cursor.execute(query)

#Creating structure
reader = open("db_structure.sql","r")
query = reader.read()
cursor.execute(query)

#Implementing functions
reader = open("functions.pgsql","r")
query = reader.read()
cursor.execute(query)

#Adding data
reader = open("data.sql","r")
query = reader.read()
cursor.execute(query)


# Close connections
conn.close()
