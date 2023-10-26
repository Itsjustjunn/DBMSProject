import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os
import csv
import re

max_price_entry = None
min_lease_entry = None
max_lease_entry = None
flat_type_entry = None
result_text = None


with open('ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv', 'r', newline='') as file:
    csv_reader = csv.DictReader(file)

def validate_login():
    login_file = open('login.txt', "r")
    username = username_entry.get()
    password = password_entry.get()

    for line in open("login.txt", "r").readlines():
        login_info = line.split()
        if username == login_info[0] and password == login_info[1]:
            messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
            username_label.pack_forget()
            username_entry.pack_forget()
            password_label.pack_forget()
            password_entry.pack_forget()
            welcome_label.pack_forget()
            # background_image.pack_forgot()
            background_label.pack_forget()
            login_button.pack_forget()

            # Show the search/filter frame
            search_frame.pack()
            return True
    messagebox.showerror("Login Failed", "Invalid username or password")
    return False


def display_stats(selected_entry):
    stats_window = tk.Toplevel(root)
    stats_window.title("Detailed Statistics")


    # Create a text widget to display the selected entry's stats
    helvetica_font = ("Helvetica", 12)
    stats_text = tk.Text(stats_window, wrap=tk.NONE, font=helvetica_font)
    stats_text.pack(fill=tk.BOTH, expand=True)
    
    # Display the selected entry's details in the new window
    for key, value in selected_entry.items():
        stats_text.insert(tk.END, f"{key}: {value}\n\n")

        
# Function to perform the search or filter operation
def search_addresses():
    global min_price_entry, max_price_entry, min_lease_entry, max_lease_entry, flat_type_entry, result_text
    keyword = search_entry.get()

    # Create a new Toplevel window for displaying results
    results_window = tk.Toplevel(root)
    results_window.title("Search Results")

    max_price_label = tk.Label(results_window, text="Max Resale Price:")
    max_price_label.pack()
    max_price_entry = tk.Entry(results_window)
    max_price_entry.pack()

    min_lease_label = tk.Label(results_window, text="Min Remaining Lease (in months):")
    min_lease_label.pack()
    min_lease_entry = tk.Entry(results_window)
    min_lease_entry.pack()

    max_lease_label = tk.Label(results_window, text="Max Remaining Lease (in months):")
    max_lease_label.pack()
    max_lease_entry = tk.Entry(results_window)
    max_lease_entry.pack()

    flat_type_label = tk.Label(results_window, text="Flat Type:")
    flat_type_label.pack()
    flat_type_entry = tk.Entry(results_window)
    flat_type_entry.pack()

    filter_button = tk.Button(results_window, text="Apply Filter", command=apply_filter)
    filter_button.pack()

    # Create a text widget for displaying the results
    helvetica_font = ("Helvetica", 12)
    result_text = tk.Text(results_window, wrap=tk.NONE, spacing1=5, spacing2=2, font=helvetica_font)
    result_text.pack(fill=tk.BOTH, expand=True)
    
    # Create a list to store the details of each matching entry
    details_list = []

    # Open the CSV file using the 'csv' module
    with open('ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv', 'r', newline='') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            if keyword.lower() in row['town'].lower():
                # Extract and format the relevant fields
                result = f"Month: {row['month']}, Town: {row['town']}, Flat Type: {row['flat_type']}, Street Name: {row['street_name']}, Storey Range: {row['storey_range']}, Flat Model: {row['flat_model']}, Lease Commence Date: {row['lease_commence_date']}, Remaining Lease: {row['remaining_lease']}, Resale Price: {row['resale_price']}"
                result_text.insert(tk.END, result + '\n')
                details_list.append(row)

    # Bind a function to each line to display detailed stats when clicked
    for i, entry in enumerate(details_list):
        result_text.tag_add(f"entry-{i}", f"{i + 1}.0", f"{i + 1}.end")
        result_text.tag_bind(f"entry-{i}", "<Button-1>", lambda event, entry=entry: display_stats(entry))


def apply_filter():
    keyword = search_entry.get().lower()
    max_price_str = max_price_entry.get()
    min_lease_str = min_lease_entry.get()
    max_lease_str = max_lease_entry.get()
    selected_flat_type = flat_type_entry.get().lower()

    max_price = float(max_price_str) if max_price_str else float("inf")

    min_lease_months = None if not min_lease_str else int(min_lease_str)
    max_lease_months = None if not max_lease_str else int(max_lease_str)

    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)

    # Create a list to store the details of each matching entry
    details_list = []

    # Open the CSV file using the 'csv' module
    with open('ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv', 'r', newline='') as file:
        csv_reader = csv.DictReader(file)

        for i, row in enumerate(csv_reader):
            town = row['town'].lower()
            resale_price = float(row['resale_price'])
            remaining_lease = row['remaining_lease']
            flat_type = row['flat_type'].lower().strip()

            # Extract the numeric parts of the remaining_lease column using regular expressions
            lease_parts = re.findall(r'\d+', remaining_lease)
            if lease_parts:
                remaining_lease_months = int(lease_parts[0])
            else:
                remaining_lease_months = 0

            if keyword in town and \
                    (max_price_str and 0 <= resale_price <= max_price) and \
                    (min_lease_months is None or min_lease_months <= remaining_lease_months) and \
                    (max_lease_months is None or remaining_lease_months <= max_lease_months) and \
                    (selected_flat_type == '' or selected_flat_type == flat_type):
                result_text.insert(tk.END,
                                   f"Month: {row['month']}, Town: {row['town']}, Flat Type: {row['flat_type']}, Street Name: {row['street_name']}, Storey Range: {row['storey_range']}, Flat Model: {row['flat_model']}, Lease Commence Date: {row['lease_commence_date']}, Remaining Lease: {remaining_lease}\n")
                details_list.append(row)

    # Bind a function to each line to display detailed stats when clicked
    for i, entry in enumerate(details_list):
        result_text.tag_add(f"entry-{i}", f"{i + 1}.0", f"{i + 1}.end")
        result_text.tag_bind(f"entry-{i}", "<Button-1>", lambda event, entry=entry: display_stats(entry))

    result_text.config(state=tk.DISABLED)


# Create the main application window
root = tk.Tk()
root.title("Property Login Page")

# set resolution
root.geometry("1920x1080")

# Load the background image using Pillow (PIL)
current_directory = os.getcwd()
relative_path = "marina.jpg"
image_path = os.path.join(current_directory, relative_path)
image = Image.open(image_path)
background_image = ImageTk.PhotoImage(image)


# Create a label to display the background image
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create an intermediate frame to center-align widgets
center_frame = tk.Frame(root)
center_frame.pack(expand=True)

# Create labels, entry widgets, and a button
welcome_label = tk.Label(root, text="Welcome\n"
                                    "Please Sign In")
welcome_label.pack()
welcome_label.config(font=('Arial',20))
username_label = tk.Label(root, text="Username:")
username_label.pack()
username_label.config(font=('Arial', 20))
username_entry = tk.Entry(root)
username_entry.pack()
password_label = tk.Label(root, text="Password:")
password_label.pack()
password_label.config(font=('Arial', 20))
password_entry = tk.Entry(root, show="*")  # Show "*" instead of actual characters for the password
password_entry.pack()

login_button = tk.Button(root, text="Login", command=validate_login)
login_button.pack()

# Create a frame for the search/filter bar
search_frame = tk.Frame(root)

# Create an entry field for search/filter
search_label = tk.Label(search_frame, text="Search:", font=('Arial', 20))
search_label.pack(side="left")

search_entry = tk.Entry(search_frame, font=('Arial', 20))
search_entry.pack(side="left")

search_button = tk.Button(search_frame, text="Search", command=search_addresses, font=('Arial', 20))
search_button.pack(side="left")

# Create a Listbox to display the search results
# result_listbox = tk.Listbox(search_frame, font=('Arial', 20))
# result_listbox.pack(side="left", fill="both", expand=True)

# # Create another spacer frame to center-align widgets horizontally
# center_spacer = tk.Frame(root)
# center_spacer.pack(expand=True)

# Create an intermediate frame to center-align widgets
center_frame = tk.Frame(root)
center_frame.pack(expand=True)
# result_listbox = tk.Listbox(search_frame, font=custom_font)
# result_listbox.pack(side="left", fill="both", expand=True)

# Start the Tkinter event loop
root.mainloop()
