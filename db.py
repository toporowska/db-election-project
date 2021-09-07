import sshtunnel 
import getpass
import psycopg2
from time import sleep

sshtunnel.SSH_TIMEOUT = sshtunnel.TUNNEL_TIMEOUT = 5.0

user = input("Username: ")
password = getpass.getpass("Password: ")

server = sshtunnel.SSHTunnelForwarder(
    ('hostadress',22),
    ssh_username=user,
    ssh_password=password,
    remote_bind_address=('db', 5432),
    local_bind_address=('127.0.0.1',1203)
)

server.start()
# A second for it to connect
sleep(1)

password = getpass.getpass("Database password: ")
conn = psycopg2.connect(database="db", password=password, user=user, host=server.local_bind_host, port= server.local_bind_port)
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Clearing existing tables and functions
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

server.stop()