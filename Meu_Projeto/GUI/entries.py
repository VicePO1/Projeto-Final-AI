import tkinter as tk


def create_entry_screenshot_size():
    global entry_screenshot_size

    entry_screenshot_size=tk.Entry(width=20)
    entry_screenshot_size.place(x=50,y=300)

def get_entry_screenshot_size():
    screenshot_size = entry_screenshot_size.get()
    return screenshot_size

def create_entry_cont(jan):
    global entry_cont
    entry_cont = tk.Entry(jan,width=20)
    entry_cont.place(x=50,y=630)

def create_entry_cap(jan):
    global entry_cap
    entry_cap = tk.Entry(jan,width=20)
    entry_cap.place(x=450,y=100)

def get_entry_cont():
    cont = entry_cont.get()
    return cont

def get_entry_cap():
    cap = entry_cap.get()
    return cap