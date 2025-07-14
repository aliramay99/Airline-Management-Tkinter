import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "airline.db"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345"

# ─── Database Operations ────────────────────────────────
def fetch_bookings():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings")
        return cursor.fetchall()

def delete_booking(booking_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
        return cursor.rowcount

def update_booking(booking_id, source, destination, date):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE bookings
            SET source = ?, destination = ?, date = ?
            WHERE id = ?
        """, (source, destination, date, booking_id))
        return cursor.rowcount

def update_flight(flight_id, airline, flight_no, origin, destination, date, time):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE flights
            SET airline = ?, flight_no = ?, origin = ?, destination = ?, date = ?, time = ?
            WHERE id = ?
        """, (airline, flight_no, origin, destination, date, time, flight_id))
        return cursor.rowcount

# ─── Admin Panel ────────────────────────────────────────
def launch_admin_panel():
    win = tk.Toplevel()
    win.title("Admin Panel - Manage Bookings")
    win.geometry("900x700")
    win.resizable(True, True)

    for i in range(20):
        win.rowconfigure(i, weight=1)
    win.columnconfigure(0, weight=1)

    tk.Label(win, text="🛠 Admin Panel: Manage Bookings & Flights", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)

    # ─── Treeview (Bookings) ──────────────────────────────
    tree_frame = tk.Frame(win)
    tree_frame.grid(row=1, column=0, sticky="nsew", padx=20)

    columns = ("ID", "Name", "Email", "From", "To", "Date")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    tree.pack(fill="both", expand=True)

    def refresh_tree():
        for row in tree.get_children():
            tree.delete(row)
        for booking in fetch_bookings():
            tree.insert("", "end", values=booking)

    refresh_tree()

    # ─── Delete Booking ──────────────────────────────────
    delete_frame = tk.LabelFrame(win, text="Delete Booking", font=("Arial", 12, "bold"), padx=10, pady=10)
    delete_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    del_id_var = tk.StringVar()
    tk.Label(delete_frame, text="Booking ID:").grid(row=0, column=0)
    tk.Entry(delete_frame, textvariable=del_id_var, width=10).grid(row=0, column=1, padx=10)

    def handle_delete():
        bid = del_id_var.get()
        if not bid.isdigit():
            messagebox.showerror("Invalid", "Please enter a numeric ID.")
            return
        if delete_booking(int(bid)):
            messagebox.showinfo("Success", f"Booking ID {bid} deleted.")
            refresh_tree()
            del_id_var.set("")
        else:
            messagebox.showwarning("Not Found", "Booking ID not found.")

    tk.Button(delete_frame, text="Delete", command=handle_delete, bg="red", fg="white").grid(row=0, column=2, padx=10)

    # ─── Edit Booking ────────────────────────────────────
    edit_frame = tk.LabelFrame(win, text="Edit Booking Info", font=("Arial", 12, "bold"), padx=10, pady=10)
    edit_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

    edit_vars = {
        "Booking ID": tk.StringVar(),
        "New From": tk.StringVar(),
        "New To": tk.StringVar(),
        "New Date (YYYY-MM-DD)": tk.StringVar()
    }

    for i, (label, var) in enumerate(edit_vars.items()):
        tk.Label(edit_frame, text=label).grid(row=i, column=0, sticky="e", pady=4)
        tk.Entry(edit_frame, textvariable=var, width=25).grid(row=i, column=1, pady=4, padx=5)

    def handle_update():
        bid = edit_vars["Booking ID"].get()
        new_from = edit_vars["New From"].get().strip()
        new_to = edit_vars["New To"].get().strip()
        new_date = edit_vars["New Date (YYYY-MM-DD)"].get().strip()

        if not (bid.isdigit() and new_from and new_to and new_date):
            messagebox.showerror("Error", "All fields must be filled correctly.")
            return

        updated = update_booking(int(bid), new_from, new_to, new_date)
        if updated:
            messagebox.showinfo("Updated", f"Booking ID {bid} updated.")
            refresh_tree()
            for var in edit_vars.values():
                var.set("")
        else:
            messagebox.showwarning("Not Found", "Booking ID not found.")

    tk.Button(edit_frame, text="Apply Changes", command=handle_update, bg="#1976D2", fg="white").grid(row=4, column=1, pady=10)

    # ─── Edit Flight ─────────────────────────────────────
    flight_frame = tk.LabelFrame(win, text="Edit Flight Info", font=("Arial", 12, "bold"), padx=10, pady=10)
    flight_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

    flight_vars = {
        "Flight ID": tk.StringVar(),
        "Airline": tk.StringVar(),
        "Flight No": tk.StringVar(),
        "From": tk.StringVar(),
        "To": tk.StringVar(),
        "Date (YYYY-MM-DD)": tk.StringVar(),
        "Time (HH:MM)": tk.StringVar()
    }

    for i, (label, var) in enumerate(flight_vars.items()):
        tk.Label(flight_frame, text=label).grid(row=i, column=0, sticky="e", pady=4)
        tk.Entry(flight_frame, textvariable=var, width=30).grid(row=i, column=1, pady=4, padx=5)

    def handle_flight_update():
        values = [var.get().strip() for var in flight_vars.values()]
        if not values[0].isdigit() or not all(values):
            messagebox.showerror("Error", "Please fill all fields correctly.")
            return

        updated = update_flight(int(values[0]), *values[1:])
        if updated:
            messagebox.showinfo("Success", f"Flight ID {values[0]} updated.")
            for var in flight_vars.values():
                var.set("")
        else:
            messagebox.showwarning("Not Found", f"Flight ID {values[0]} not found.")

    tk.Button(flight_frame, text="Update Flight", command=handle_flight_update, bg="#1976D2", fg="white").grid(row=7, column=1, pady=10)

# ─── Secure Launch Entry ────────────────────────────────
def launch_admin_panel_with_login():
    login_win = tk.Toplevel()
    login_win.title("Admin Login")
    login_win.geometry("300x200")
    login_win.resizable(False, False)

    tk.Label(login_win, text="Admin Login", font=("Arial", 14, "bold")).pack(pady=10)

    username_var = tk.StringVar()
    password_var = tk.StringVar()

    tk.Label(login_win, text="Username:").pack()
    tk.Entry(login_win, textvariable=username_var).pack(pady=5)

    tk.Label(login_win, text="Password:").pack()
    tk.Entry(login_win, textvariable=password_var, show="*").pack(pady=5)

    def validate():
        if username_var.get() == ADMIN_USERNAME and password_var.get() == ADMIN_PASSWORD:
            login_win.destroy()
            launch_admin_panel()
        else:
            messagebox.showerror("Access Denied", "Invalid admin credentials.")

    tk.Button(login_win, text="Login", command=validate, bg="#1976D2", fg="white").pack(pady=10)
