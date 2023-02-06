import unittest
import youtube_scraper
import youtube_gui
import sqlite3
import datetime
import json


class TestYouTubeGui(unittest.TestCase):
    def test_create_database(self):
        youtube_gui.create_database()
        conn = sqlite3.connect("youtube_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        result = cursor.fetchall()
        self.assertIn(("youtubers",), result)

    def test_add_to_database(self):
        youtube_gui.add_to_database("test", 1000)
        conn = sqlite3.connect("youtube_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, subscribers, timestamp FROM youtubers WHERE name=?", ("test",))
        result = cursor.fetchall()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "test")
        self.assertEqual(result[0][1], 1000)
        self.assertIsInstance(result[0][2], str)
        self.assertEqual(datetime.datetime.strptime(result[0][2], "%Y-%m-%d %H:%M:%S.%f"), 
                 datetime.datetime.strptime(result[0][2], "%Y-%m-%d %H:%M:%S.%f"))


class TestYouTubeScraper(unittest.TestCase):

    def test_get_sub_count(self):
        sub_count = youtube_scraper.get_sub_count("testuser")
        self.assertIsNotNone(sub_count)
        self.assertIsInstance(sub_count, str)
        self.assertGreaterEqual(len(sub_count), 4000)
