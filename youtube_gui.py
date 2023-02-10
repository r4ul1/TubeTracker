import tkinter as tk
import sqlite3
import datetime
import youtube_scraper

# Function to create the database 'youtube_database.db' if it does not exist.
def create_database():
    # Connect to the database.
    conn = sqlite3.connect("youtube_database.db")
    cursor = conn.cursor()

    # Create the table 'youtubers' if it does not exist.
    cursor.execute("""CREATE TABLE IF NOT EXISTS youtubers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            subscribers INTEGER,
            recentvideo TEXT,
            views INTEGER,
            timestamp TEXT)
        """)

    # Confirm that the database was created successfully.
    print("Database created successfully.")
    conn.close()

# Function to add/update the data of a YouTube channel in the database.
def add_to_database(name, subscribers, recentvideo, views):
    # Connect to the database.
    conn = sqlite3.connect("youtube_database.db")
    cursor = conn.cursor()

    # Create the table 'youtubers' if it does not exist.
    cursor.execute("CREATE TABLE IF NOT EXISTS youtubers (name text, subscribers integer, timestamp datetime, recentvideo text, views integer DEFAULT CURRENT_TIMESTAMP)")

    # Get the current timestamp.
    timestamp = str(datetime.datetime.now())

    # Check if the channel already exists in the database.
    cursor.execute("SELECT * FROM youtubers WHERE name=?", (name,))
    data = cursor.fetchall()

    # If the channel does not exist, insert the data.
    if len(data) == 0:
        cursor.execute("""INSERT INTO youtubers (name, subscribers, recentvideo, views, timestamp)
                        VALUES (?,?,?)
                    """, (name, subscribers, recentvideo, views, timestamp))
    # If the channel already exists, update the data.
    else:
        cursor.execute("""UPDATE youtubers SET subscribers=?, timestamp=?, recentvideo=?, views=?, WHERE name=?
                    """, (subscribers, timestamp, recentvideo, views, name))

    # Commit the changes and close the connection to the database.
    conn.commit()
    print("Data added/updated successfully.")
    conn.close()

# Function to search for the number of subscribers of a YouTube channel using the YouTube scraper.
def search_yt():
    # Get the channel name entered by the user.
    name = entry.get()
    
    # Get the number of subscribers using the YouTube scraper.
    subscribers = youtube_scraper.get_sub_count(name)

    recentvideo = youtube_scraper.get_most_recent_video_views(name)

    views = youtube_scraper.get_most_recent_video_views(name)

    # Add/update the data of the channel in the database.
    add_to_database(name, subscribers, recentvideo, views)
    
    # Update the result label with the number of subscribers of the channel.
    result_label.config(text=f"{name} hat {subscribers} Abonennten.")
    result_label.config(text=f"Das letzte Video von {name} heißt |{recentvideo}| und hat {views}.")

root = tk.Tk()
root.title("Tube Tracker")
root.configure(bg="#333")

title = tk.Label(root, text="Tube", font=("Helvetica", 20), bg="#333", fg="red")
title.pack(pady=20, side="left")

title = tk.Label(root, text="Tracker", font=("Helvetica", 20), bg="#333", fg="#fff")
title.pack(pady=20, side="left")

frame = tk.Frame(root, bg="#333")
frame.pack()

label = tk.Label(frame, text="Suche nach einem Youtuber:", bg="#333", fg="#fff")
label.pack()

entry = tk.Entry(frame)
entry.pack()

button = tk.Button(frame, text="Suchen", command=search_yt)
button.pack()

result_label = tk.Label(frame, text="", bg="#333", fg="#fff")
result_label.pack()

root.mainloop()
