import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def fetch_bookings():
    """Fetch all bookings from the SQLite database."""
    try:
        conn = sqlite3.connect("airline.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings")
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return []

def launch_view_bookings_window():
    """Launch the View Bookings window."""
    window = tk.Tk()
    window.title("View Booked Tickets")
    window.geometry("700x400")
    window.resizable(False, False)

    tk.Label(window, text="Booked Tickets", font=("Arial", 16)).pack(pady=10)

    columns = ("ID", "Name", "Email", "From", "To", "Date")
    tree = ttk.Treeview(window, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    bookings = fetch_bookings()
    for booking in bookings:
        tree.insert("", tk.END, values=booking)

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    window.mainloop()

if __name__ == "__main__":
    launch_view_bookings_window()
