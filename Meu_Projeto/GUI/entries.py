import tkinter as tk

def create_entry_screenshot_size():
    global entry_screenshot_size

    entry_screenshot_size=tk.Entry(width=20)
    entry_screenshot_size.place(x=50,y=300)

def get_entry_screenshot_size():
    screenshot_size = entry_screenshot_size.get()
    return screenshot_size
