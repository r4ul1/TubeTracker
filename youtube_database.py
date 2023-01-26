import sqlite3
import datetime

# Connect to or create the database
conn = sqlite3.connect('youtube_channels.db')
c = conn.cursor()

# Create the table to store channel information
c.execute('''CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY, name TEXT, subscriber_count INTEGER, timestamp DATETIME)''')

# Function to insert channel information into the database
def insert_channel_info(channel_id, channel_name, subscriber_count):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO channels (id, name, subscriber_count, timestamp) VALUES (?, ?, ?, ?)", (channel_id, channel_name, subscriber_count, timestamp))
    conn.commit()
    
# Function to retrieve channel information from the database
def retrieve_channel_info(name):
    c.execute("SELECT id, subscriber_count, timestamp FROM channels WHERE name=?", (name,))
    channel_info = c.fetchone()
    return channel_info
