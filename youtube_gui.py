import sys
import tkinter as tk
from tkinter import ttk
import youtube_scraper
import youtube_database

def get_subscriber_count(entry_name):
    name = entry_name.get()
    channel_id = youtube_scraper.get_channel_id(name)
    subscriber_count = youtube_scraper.get_channel_subscriber_count(name)
    youtube_database.insert_channel_info(channel_id, name, subscriber_count)
    display_subscriber_count(subscriber_count)

def display_subscriber_count(subscriber_count):
        global label_subscriber_count
        label_subscriber_count.config(text="Subscriber Count: " + str(subscriber_count))

def main():
    root = tk.Tk()
    root.title("Tube Tracker")
    
    label_name = ttk.Label(root, text="Enter channel name:")
    label_name.grid(row=0, column=0, padx=10, pady=10)

    entry_name = ttk.Entry(root)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    button_search = ttk.Button(root, text="Search", command=lambda: get_subscriber_count(entry_name))
    button_search.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    global label_subscriber_count
    label_subscriber_count = ttk.Label(root, text="Subscriber Count:")
    label_subscriber_count.grid(row=2, column=0, padx=10, pady=10)

    root.mainloop()

if __name__ == '__main__':
    sys.exit(main())
