import sqlite3
from datetime import datetime

class CRUD:
    def init(self):
        self.conn = sqlite3.connect("youtube_database.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS subscribers (name TEXT, subscriber_count INTEGER, timestamp DATETIME)")
        self.conn.commit()

    def insert_data(self, name, subscriber_count):
        current_time = datetime.now()
        self.cursor.execute(
            "INSERT INTO subscribers (name, subscriber_count, timestamp) VALUES (?,?,?)", (name, subscriber_count, current_time))
        self.conn.commit()

    def update_data(self, name, subscriber_count):
        current_time = datetime.now()
        self.cursor.execute(
            "UPDATE subscribers SET subscriber_count=?, timestamp=? WHERE name=?", (subscriber_count, current_time, name))
        self.conn.commit()

    def read_data(self):
        self.cursor.execute("SELECT * FROM subscribers")
        return self.cursor.fetchall()

    def delete_data(self, name):
        self.cursor.execute("DELETE FROM subscribers WHERE name=?", (name,))
        self.conn.commit()

