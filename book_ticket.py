import tkinter as tk
from tkinter import messagebox
import sqlite3

DB_NAME = "airline.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                source TEXT NOT NULL,
                destination TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)

def insert_booking(name, email, source, destination, date):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bookings (name, email, source, destination, date)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, source, destination, date))

def launch_book_ticket_window():
    init_db()

    win = tk.Toplevel()
    win.title("Book Ticket")
    win.geometry("550x550")
    win.configure(bg="#e0f7fa")  # Light blue background
    win.minsize(500, 500)

    # Title
    tk.Label(
        win,
        text="✈️ Book Your Ticket",
        font=("Arial", 20, "bold"),
        bg="#e0f7fa",
        fg="#01579b"
    ).pack(pady=20)

    # Form Frame with white background
    form_frame = tk.LabelFrame(
        win,
        text="Passenger Information",
        font=("Arial", 12, "bold"),
        padx=20, pady=20,
        bg="white",
        fg="#0277bd",
        bd=2,
        relief="groove"
    )
    form_frame.pack(padx=30, pady=10, fill="both", expand=True)

    # Variables
    name_var = tk.StringVar()
    email_var = tk.StringVar()
    source_var = tk.StringVar()
    dest_var = tk.StringVar()
    date_var = tk.StringVar()

    entries = {
        "Full Name": name_var,
        "Email": email_var,
        "From": source_var,
        "To": dest_var,
        "Date (YYYY-MM-DD)": date_var
    }

    for i, (label, var) in enumerate(entries.items()):
        tk.Label(form_frame, text=label, font=("Arial", 11), bg="white").grid(row=i, column=0, sticky="e", padx=10, pady=8)
        tk.Entry(form_frame, textvariable=var, font=("Arial", 11), width=30).grid(row=i, column=1, padx=10, pady=8)

    def clear_fields():
        for var in entries.values():
            var.set("")

    def book_ticket():
        values = [v.get().strip() for v in entries.values()]
        if not all(values):
            messagebox.showerror("Input Error", "All fields are required.")
            return
        try:
            insert_booking(*values)
            messagebox.showinfo("Success", "Ticket booked successfully!")
            clear_fields()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # Book Button
    tk.Button(
        win,
        text="Book Ticket",
        command=book_ticket,
        font=("Arial", 12, "bold"),
        bg="#00796b",
        fg="white",
        activebackground="#004d40",
        padx=15, pady=8
    ).pack(pady=20)

    # Footer
    tk.Label(
        win,
        text="Powered by Airline System",
        font=("Arial", 10),
        bg="#e0f7fa",
        fg="gray"
    ).pack(side="bottom", pady=10)
