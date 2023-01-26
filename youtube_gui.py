from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
from youtube_scraper import get_channel_id, get_subscriber_count
from youtube_database import insert_channel_info, retrieve_channel_info
import sqlite3
import sys
import datetime

class YouTubeSubscriberCounter(QWidget):

    def __init__(self, argv):
        super().__init__()
        self.app = QApplication(argv)
        
        self.conn = sqlite3.connect('youtube_channels.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY, name TEXT, subscriber_count INTEGER, timestamp DATETIME)''')
        
        self.channel_name = QLineEdit()
        self.channel_name.setPlaceholderText("Enter YouTube channel name")
        self.channel_name.returnPressed.connect(self.search)
        
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search)
        
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update)
        
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        
        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(self.channel_name)
        self.search_layout.addWidget(self.search_button)
        self.search_layout.addWidget(self.update_button)
        
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.search_layout)
        self.main_layout.addWidget(self.result_label)
        self.setLayout(self.main_layout)

    def search(self):
        name = self.channel_name.text()
        channel_info = retrieve_channel_info(name)

        if channel_info:
            self.result_label.setText(f"Subscribers: {channel_info[1]}\nLast updated: {channel_info[2]}")
        else:
            channel_id = get_channel_id(name)
            subscriber_count = get_subscriber_count(channel_id)
            insert_channel_info(channel_id, name, subscriber_count)
            self.result_label.setText(f"Subscribers: {subscriber_count}")


    def update(self):
        name = self.channel_name.text()
        channel_id = get_channel_id(name)
        subscriber_count = get_subscriber_count(channel_id)
        insert_channel_info(channel_id, name, subscriber_count)
        self.result_label.setText(f"Subscribers: {subscriber_count}\nLast updated: {datetime.datetime.now()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = YouTubeSubscriberCounter(sys.argv)
    gui.show()
    sys.exit(app.exec_())
