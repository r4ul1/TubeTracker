import unittest
import youtube_scraper
import youtube_gui
import sqlite3
import datetime


# Test for youtube_gui.py
class TestYouTubeGui(unittest.TestCase):
    # Test the create_database function
    def test_create_database(self):
        # Call the create_database function
        youtube_gui.create_database()

        # Connect to the database
        conn = sqlite3.connect("youtube_database.db")
        cursor = conn.cursor()
        
        # Check if the table "youtubers" was created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        result = cursor.fetchall()
        self.assertIn(("youtubers",), result)

    # Test the add_to_database function
    def test_add_to_database(self):
        # Call the add_to_database function with the name "test" and subscriber count 1000
        youtube_gui.add_to_database("test", 1000)

        # Connect to the database
        conn = sqlite3.connect("youtube_database.db")
        cursor = conn.cursor()
        
        # Fetch the data for the name "test"
        cursor.execute("SELECT name, subscribers, timestamp FROM youtubers WHERE name=?", ("test",))
        result = cursor.fetchall()
        
        # Check if there is only one result
        self.assertEqual(len(result), 1)
        # Check if the name is "test"
        self.assertEqual(result[0][0], "test")
        # Check if the subscriber count is 1000
        self.assertEqual(result[0][1], 1000)
        # Check if the timestamp is a string
        self.assertIsInstance(result[0][2], str)
        # Check if the timestamp can be parsed into a datetime object
        self.assertEqual(datetime.datetime.strptime(result[0][2], "%Y-%m-%d %H:%M:%S.%f"), 
                 datetime.datetime.strptime(result[0][2], "%Y-%m-%d %H:%M:%S.%f"))


# Test for youtube_scraper.py
class TestYouTubeScraper(unittest.TestCase):

    # Test the get_sub_count function
    def test_get_sub_count(self):
        # Call the get_sub_count function with the name "R4uul"
        sub_count = youtube_scraper.get_sub_count("R4uul")
        
        # Check if the subscriber count is not None
        self.assertIsNotNone(sub_count, "Subscriber count should not be None.")
        # Check if the subscriber count is a string
        self.assertIsInstance(sub_count, str, "Subscriber count should be a string.")
        # Check if the subscriber count has at least one character
        self.assertGreaterEqual(len(sub_count), 1, "Subscriber count should have at least one character.")
