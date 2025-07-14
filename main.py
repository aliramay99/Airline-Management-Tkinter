import tkinter as tk
from book_ticket import launch_book_ticket_window
from view_bookings import launch_view_bookings_window
from admin_panel import launch_admin_panel_with_login
from flight import launch_flight_page

def main_menu():
    root = tk.Tk()
    root.title("Airline Management System")
    root.geometry("500x500")
    root.minsize(400, 400)

    # Configure rows and columns to expand with window
    root.columnconfigure(0, weight=1)
    for i in range(8):
        root.rowconfigure(i, weight=1)

    # Title label
    tk.Label(
        root,
        text="✈️ Airline Management System",
        font=("Arial", 18, "bold")
    ).grid(row=0, column=0, pady=20, sticky="n")

    # Button style function
    def create_button(text, command, row):
        tk.Button(
            root,
            text=text,
            command=command,
            font=("Arial", 12),
            bg="#1976D2",
            fg="white",
            activebackground="#0D47A1",
            padx=10,
            pady=10
        ).grid(row=row, column=0, padx=60, sticky="ew")

    # Navigation buttons
    create_button("View Flights", launch_flight_page, 2)
    create_button("Book Ticket", launch_book_ticket_window, 3)
    create_button("View Bookings", launch_view_bookings_window, 4)
    create_button("Admin Panel (Delete Bookings)", launch_admin_panel_with_login, 5)

    # Footer
    tk.Label(
        root,
        text="Created by: Ali Hassan",
        font=("Arial", 10),
        fg="gray"
    ).grid(row=7, column=0, pady=20, sticky="s")

    root.mainloop()

if __name__ == "__main__":
    main_menu()
