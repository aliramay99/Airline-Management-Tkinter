import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def fetch_bookings():
    try:
        with sqlite3.connect("airline.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bookings")
            return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return []

def launch_view_bookings_window():
    win = tk.Toplevel()
    win.title("View Bookings")
    win.geometry("700x400")

    tk.Label(win, text="Booked Tickets", font=("Arial", 16)).pack(pady=10)

    columns = ["ID", "Name", "Email", "From", "To", "Date"]
    tree = ttk.Treeview(win, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    for row in fetch_bookings():
        tree.insert("", "end", values=row)
