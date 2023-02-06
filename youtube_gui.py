import tkinter as tk
import sqlite3
import datetime
import youtube_scraper


def create_database():
    conn = sqlite3.connect("youtube_database.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS youtubers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            subscribers INTEGER,
            timestamp TEXT)
        """)

    print("Database created successfully.")
    conn.close()


def add_to_database(name, subscribers):
    conn = sqlite3.connect("youtube_database.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS youtubers (name text, subscribers integer, timestamp datetime DEFAULT CURRENT_TIMESTAMP)")

    timestamp = str(datetime.datetime.now())

    cursor.execute("SELECT * FROM youtubers WHERE name=?", (name,))
    data = cursor.fetchall()
    if len(data) == 0:
        cursor.execute("""INSERT INTO youtubers (name, subscribers, timestamp)
                        VALUES (?,?,?)
                    """, (name, subscribers, timestamp))
    else:
        cursor.execute("""UPDATE youtubers SET subscribers=?, timestamp=? WHERE name=?
                    """, (subscribers, timestamp, name))

    conn.commit()
    print("Data added/updated successfully.")
    conn.close()


def search_yt():
    name = entry.get()
    subscribers = youtube_scraper.get_sub_count(name)
    add_to_database(name, subscribers)
    result_label.config(text=f"{name} has {subscribers} subscribers.")

root = tk.Tk()
root.title("Tube Tracker")
root.configure(bg="#333")

title = tk.Label(root, text="Tube", font=("Helvetica", 20), bg="#333", fg="red")
title.pack(pady=20, side="left")

title = tk.Label(root, text="Tracker", font=("Helvetica", 20), bg="#333", fg="#fff")
title.pack(pady=20, side="left")

frame = tk.Frame(root, bg="#333")
frame.pack()

label = tk.Label(frame, text="Enter a YouTube username:", bg="#333", fg="#fff")
label.pack()

entry = tk.Entry(frame)
entry.pack()

button = tk.Button(frame, text="Search", command=search_yt)
button.pack()

result_label = tk.Label(frame, text="", bg="#333", fg="#fff")
result_label.pack()

root.mainloop()
