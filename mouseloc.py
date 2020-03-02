import tkinter as tk

root = tk.Tk()

while True:
    x = root.winfo_pointerx()
    y = root.winfo_pointery()
    abs_coord_x = root.winfo_pointerx() - root.winfo_rootx()
    abs_coord_y = root.winfo_pointery() - root.winfo_rooty()

    return x, y
