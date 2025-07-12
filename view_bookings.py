import sqlite3
import tkinter as tk
from tkinter import ttk

def view_bookings():
    root = tk.Tk()
    root.title("View Bookings")
    root.geometry("700x400")

    title = tk.Label(root, text="All Bookings", font=("Arial", 18, "bold"))
    title.pack(pady=10)

    cols = ("ID", "Passenger Name", "Flight No", "Date", "Seat No")
    tree = ttk.Treeview(root, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill=tk.BOTH, expand=True)

    conn = sqlite3.connect("airline.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

    conn.close()
    root.mainloop()

if __name__ == "__main__":
    view_bookings()
