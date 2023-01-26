import sqlite3
import datetime

class YouTubeDatabase:

    def __init__(self):
        self.conn = sqlite3.connect('youtube_channels.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY, name TEXT, subscriber_count INTEGER, timestamp DATETIME)''')

    def create(self, channel_id, channel_name, subscriber_count):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.c.execute("INSERT INTO channels (id, name, subscriber_count, timestamp) VALUES (?, ?, ?, ?)", (channel_id, channel_name, subscriber_count, timestamp))
        self.conn.commit()

    def read(self, name):
        self.c.execute("SELECT id, subscriber_count, timestamp FROM channels WHERE name=?", (name,))
        channel_info = self.c.fetchone()
        return channel_info

    def update(self, channel_id, channel_name, subscriber_count):
        self.c.execute("UPDATE channels SET name=?, subscriber_count=?, timestamp=? WHERE id=?", (channel_name, subscriber_count, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), channel_id))
        self.conn.commit()

    def delete(self, channel_id):
        self.c.execute("DELETE FROM channels WHERE id=?", (channel_id,))
        self.conn.commit()

    def retrieve(self, channel_id):
        self.c.execute("SELECT id, name, subscriber_count, timestamp FROM channels WHERE id=?", (channel_id,))
        channel_info = self.c.fetchone()
        return channel_info
