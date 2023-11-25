import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
import pyodbc
import re
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from pymongo import MongoClient

#Database connections
########################################################################################################################
# Connect to MSSQL database using Windows Authentication
connection_config = {
    'driver': '{SQL Server}',
    'server': 'DESKTOP-N93S83Q',
    'database': 'DBMSTest',
    'trusted_connection': 'yes'  # Use Windows Authentication
}

conn_str = 'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection}'.format(**connection_config)
conn = pyodbc.connect(conn_str)

# client = MongoClient('localhost', 27017)
# db = client['DBMSProjectUsers']
# collection = db['collection_users']
########################################################################################################################

def fetch_data_after_login():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor() #problem here
        search_addresses(cursor, 'Property')

    except pyodbc.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the database connection in the 'finally' block to ensure it's closed even if an exception occurs
        if 'conn' in locals() and conn:
            conn.close()


def show_data_window(rows):
    data_window = tk.Toplevel(root)
    data_window.title("Data from MSSQL")

    # Create a Treeview widget to display the data
    tree = ttk.Treeview(data_window, columns=list(range(len(rows[0]))), show="headings", height=10)

    # Set column headings
    for i, heading in enumerate(rows[0]):
        tree.heading(i, text=heading)
        tree.column(i, anchor=tk.CENTER, width=100)

    # Insert data into the Treeview
    for row in rows[1:]:
        # Convert each item in the row to a string
        string_row = [str(item) for item in row]
        tree.insert("", "end", values=string_row)

    tree.pack(expand=True, fill=tk.BOTH)

def validate_login():

    username = username_entry.get()
    password = password_entry.get()

    client = MongoClient('localhost', 27017)
    db = client['DBMSProjectUsers']
    collection = db['collection_users']

    # Query MongoDB for the provided username
    user_document = collection.find_one({"userid": username})

    if user_document:
        # User found, check if the provided password matches
        if user_document["password"] == password:
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


def check_user_role():
    # Connect to MongoDB
    client = MongoClient('localhost', 27017)
    db = client['DBMSProjectUsers']
    collection = db['collection_users']

    # Query MongoDB for the currently logged-in user
    userid = username_entry.get()
    user_document = collection.find_one({"userid": userid})

    if user_document:
        # Check the role of the user
        user_role = user_document.get("role", "")
        return user_role


def check_user_id():
    # Connect to MongoDB
    client = MongoClient('localhost', 27017)
    db = client['DBMSProjectUsers']
    collection = db['collection_users']

    # Query MongoDB for the currently logged-in user
    userid = username_entry.get()
    user_document = collection.find_one({"userid": userid})

    if user_document:
        # Return the userid of the user
        return user_document.get("userid", "")


def check_user_name():
    # Connect to MongoDB
    client = MongoClient('localhost', 27017)
    db = client['DBMSProjectUsers']
    collection = db['collection_users']

    # Query MongoDB for the currently logged-in user
    userid = username_entry.get()
    user_document = collection.find_one({"userid": userid})

    if user_document:
        # Check the role of the user
        user_name = user_document.get("name", "")
        return user_name
def get_user_list_from_mongodb():
    try:
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['DBMSProjectUsers']
        collection = db['collection_users']

        # Retrieve all users from the collection
        users = collection.find({}, {"_id": 0, "userid": 1})

        # Convert the cursor to a list of dictionaries
        user_list = list(users)

        return user_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def validate_login_and_fetch_data():
    if validate_login():
        # If login is successful, fetch and display data
        fetch_data_after_login()


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

    if check_user_role() == "agent" or check_user_role() == "admin":

        # Create a button to edit the property
        buyers_button = tk.Button(stats_window, text="View Interested Buyers", command=lambda: display_interested_buyers(selected_entry['property_id']))
        buyers_button.pack(side="left")
        # Create a button to edit the property
        update_button = tk.Button(stats_window, text="Update Property", command=lambda: update_property(selected_entry))
        update_button.pack(side="right")

        # Create a button to delete the property
        delete_button = tk.Button(stats_window, text="Delete Property",
                                  command=lambda: delete_property(selected_entry['property_id'], stats_window))
        delete_button.pack(side="right")

    elif (check_user_role() == "buyer"):
        interest_button = tk.Button(stats_window, text="Show Interest", command=lambda: show_interest(conn.cursor(), selected_entry['property_id']))
        interest_button.pack(side="right")


def search_addresses(cursor, table_name):
    global min_price_entry, max_price_entry, min_lease_entry, max_lease_entry, flat_type_entry, result_text
    keyword = search_entry.get()

    # Create a new Toplevel window for displaying results
    results_window = tk.Toplevel(root)
    results_window.title("Properties")
    # Set the window to full screen
    results_window.attributes('-fullscreen', True)

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

    filter_button = tk.Button(results_window, text="Apply Filter", command=lambda: apply_filter(cursor, table_name))
    filter_button.pack()

    if check_user_role() == "admin":
        view_audit_log_button = tk.Button(results_window, text="View Audit Log", command=show_audit_log)
        view_audit_log_button.place(relx=0.00, rely=0.00, anchor="nw")
        # Create buttons for admin tasks
        add_user_button = tk.Button(results_window, text="Add User", command=add_user_window)
        add_user_button.place(relx=0.00, rely=0.22, anchor="nw")

        delete_user_button = tk.Button(results_window, text="Delete User", command=delete_user_window)
        delete_user_button.place(relx=0.04, rely=0.22, anchor="nw")

    if check_user_role() == "agent" or check_user_role() == "admin":
        add_property_button = tk.Button(results_window, text="Add Property", command=add_property_window)
        add_property_button.pack(anchor="ne")

    user_info_button = tk.Button(results_window, text="Show User Info", command=show_user_info)
    user_info_button.place(relx=1, rely=0.00, anchor="ne")
    # Create a logout button
    logout_button = tk.Button(results_window, text="Logout", command=lambda: logout(results_window))
    logout_button.place(relx=0.94, rely=0.00, anchor="ne")

    # Create a text widget for displaying the results
    helvetica_font = ("Helvetica", 12)
    result_text = tk.Text(results_window, wrap=tk.NONE, spacing1=5, spacing2=2, font=helvetica_font)
    result_text.pack(fill=tk.BOTH, expand=True)

    # Create a list to store the details of each matching entry
    details_list = []

    # Execute the SQL query to fetch data from the database table
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    column_names = [column[0] for column in cursor.description]
    rows_as_dicts = [dict(zip(column_names, row)) for row in rows]

    for row in rows_as_dicts:
        if keyword.lower() in str(row['town']).lower():
            # Extract and format the relevant fields
            result = f"Month: {row['month']}, Town: {row['town']}, Flat Type: {row['flat_type']}, Street Name: {row['street_name']}, Storey Range: {row['storey_range']}, Flat Model: {row['flat_model']}, Lease Commence Date: {row['lease_commence_date']}, Remaining Lease: {row['remaining_lease']}, Resale Price: {row['resale_price']}"
            result_text.insert(tk.END, result + '\n')
            details_list.append(row)

    # Bind a function to each line to display detailed stats when clicked
    for i, entry in enumerate(details_list):
        result_text.tag_add(f"entry-{i}", f"{i + 1}.0", f"{i + 1}.end")
        result_text.tag_bind(f"entry-{i}", "<Button-1>", lambda event, entry=entry: display_stats(entry))


def apply_filter(cursor, table_name):
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

    # Execute the SQL query to fetch data from the database table
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    column_names = [column[0] for column in cursor.description]
    rows_as_dicts = [dict(zip(column_names, row)) for row in rows]

    for i, row in enumerate(rows_as_dicts):
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


def add_property_window():
    add_window = tk.Toplevel(root)
    add_window.title("Add Property")

    # Fetch the last property_id from the database
    last_property_id = get_last_property_id()

    # Calculate the new property_id (max + 1)
    new_property_id = last_property_id + 1

    # Create labels and entry widgets for property details
    property_details = ['property_id', 'month', 'town', 'flat_Type', 'block', 'street_name', 'storey_range', 'floor_area_sqm', 'flat_model',
                        'lease_commence_date', 'remaining_lease', 'resale_price']

    entry_widgets = {}

    # Insert the next property_id in the property_details list
    for i, detail in enumerate(property_details):
        label = tk.Label(add_window, text=f"{detail}:", font=('Arial', 12))
        label.grid(row=i, column=0, padx=10, pady=5, sticky="e")

        # Use the calculated property_id for the 'property_id' entry
        entry_value = new_property_id if detail == 'property_id' else ''
        entry = tk.Entry(add_window, font=('Arial', 12))
        entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        entry.insert(0, entry_value)  # Pre-fill the 'property_id' field

        entry_widgets[detail] = entry

    # Create a button to save the property details
    save_button = tk.Button(add_window, text="Save", command=lambda: save_property(entry_widgets, add_window, new_property_id))
    save_button.grid(row=len(property_details), columnspan=2, pady=10)


def save_property(entry_widgets, add_window, new_property_id):
    # Retrieve the property details from the entry widgets
    property_data = {detail: entry.get() for detail, entry in entry_widgets.items()}

    # Validate the data (you can add more validation if needed)

    # Insert the property data into the database
    insert_property_into_database(property_data, add_window, new_property_id)


def insert_property_into_database(property_data, add_window, new_property_id):
    try:
        cursor = conn.cursor()

        # Modify the following SQL query to match your table structure
        query = "INSERT INTO Property ([property_id], month, town, [flat_type], block, [street_name], [storey_range], " \
                "[floor_area_sqm], [flat_model], [lease_commence_date], [remaining_lease], [resale_price]) " \
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        # Extract values from the property_data dictionary and pass them as parameters to the query
        cursor.execute(query, tuple(property_data.values()))

        # Commit the changes to the database
        conn.commit()

        # Close the update window after successful update
        add_window.destroy()
        # Notify the user that the property has been added
        messagebox.showinfo("Success", "Property added successfully!")
        log_user_action(check_user_id(), check_user_name(), "Added Property: " + str(new_property_id),cursor)

    except pyodbc.Error as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", "Failed to add property.")

    finally:
        # Close the database connection
        if 'conn' in locals() and conn:
            conn.close()


def get_last_property_id():
    try:
        cursor = conn.cursor()
        query = "SELECT MAX(property_id) FROM dbo.property"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        return result if result is not None else 0
    except pyodbc.Error as e:
        print(f"An error occurred while fetching the last property_id: {e}")
        return 0
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()


def update_property(selected_entry):
    update_window = tk.Toplevel(root)
    update_window.title("Update Property")

    # Create labels and entry widgets for property details
    property_details = ['property_id', 'month', 'town', 'flat_type', 'block', 'street_name', 'storey_range', 'floor_area_sqm', 'flat_model',
                        'lease_commence_date', 'remaining_lease', 'resale_price']

    entry_widgets = {}

    for i, detail in enumerate(property_details):
        label = tk.Label(update_window, text=f"{detail}:", font=('Arial', 12))
        label.grid(row=i, column=0, padx=10, pady=5, sticky="e")

        # Use the value from the selected entry for each detail
        entry_value = selected_entry.get(detail, '')
        entry = tk.Entry(update_window, font=('Arial', 12))
        entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        entry.insert(0, entry_value)  # Pre-fill the entry with the selected value

        entry_widgets[detail] = entry

    # Create a button to save the updated property details
    save_button = tk.Button(update_window, text="Save", command=lambda: save_updated_property(entry_widgets, update_window))
    save_button.grid(row=len(property_details), columnspan=2, pady=10)

def save_updated_property(entry_widgets, update_window):
    # Retrieve the values from entry widgets
    property_id = entry_widgets['property_id'].get()
    month = entry_widgets['month'].get()
    town = entry_widgets['town'].get()
    flattype = entry_widgets['flat_type'].get()
    block = entry_widgets['block'].get()
    streetname = entry_widgets['street_name'].get()
    storeyrange = entry_widgets['storey_range'].get()
    floorareasqm = entry_widgets['floor_area_sqm'].get()
    flatmodel = entry_widgets['flat_model'].get()
    leasecommencedate = entry_widgets['lease_commence_date'].get()
    remaininglease = entry_widgets['remaining_lease'].get()
    resaleprice = entry_widgets['resale_price'].get()
    # ... (repeat for other details)

    # Construct an SQL UPDATE statement
    update_query = (f"UPDATE Property SET month='{month}', town='{town}', flat_type='{flattype}' , "
                    f"block='{block}' , street_name='{streetname}', storey_range='{storeyrange}', "
                    f"floor_area_sqm='{floorareasqm}', flat_model='{flatmodel}', lease_commence_date='{leasecommencedate}', "
                    f" remaining_lease='{remaininglease}', resale_price='{resaleprice}' WHERE property_id='{property_id}'")

    try:
        # Execute the update query using your database connection
        cursor = conn.cursor()
        cursor.execute(update_query)
        conn.commit()

        # Close the update window after successful update
        update_window.destroy()
        # Notify the user that the property has been added
        messagebox.showinfo("Success", "Property updated successfully!")
        log_user_action(check_user_id(), check_user_name(), "Edited Property: " + str(property_id), cursor)

    except pyodbc.Error as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", "Failed to update property.")

    finally:
        # Close the database connection
        if 'conn' in locals() and conn:
            conn.close()


def delete_property(property_id, stats_window):
    # Prompt the user for confirmation
    response = messagebox.askyesno("Confirmation", f"Do you really want to delete Property ID {property_id}?")

    if response:
        # Construct an SQL DELETE statement
        delete_query = f"DELETE FROM Property WHERE property_id='{property_id}'"

        try:
            # Execute the delete query using your database connection
            cursor = conn.cursor()
            cursor.execute(delete_query)
            conn.commit()

            stats_window.destroy()
            # Notify the user that the property has been added
            messagebox.showinfo("Success", "Property deleted successfully!")
            log_user_action(check_user_id(), check_user_name(), "Deleted Property: " + str(property_id), cursor)


        except pyodbc.Error as e:
            print(f"An error occurred: {e}")
            messagebox.showerror("Error", "Failed to delete property.")

        finally:
            # Close the database connection
            if 'conn' in locals() and conn:
                conn.close()


def fetch_interested_buyers(property_id):
    cursor = conn.cursor()
    # Execute the SQL query to fetch interested buyers for the selected property_id
    query = f"SELECT * FROM Property_Buyer WHERE property_id = {property_id}"
    cursor.execute(query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    column_names = [column[0] for column in cursor.description]
    rows_as_dicts = [dict(zip(column_names, row)) for row in rows]

    # Connect to MongoDB
    client = MongoClient('localhost', 27017)
    db = client['DBMSProjectUsers']
    collection = db['collection_users']

    user_ids = [result['userid'] for result in rows_as_dicts]

    # Fetch usernames from MongoDB using user IDs
    interested_buyers = []
    for user_id in user_ids:
        user_data = collection.find_one({"userid": user_id})
        if user_data:
            interested_buyers.append("Name: " + user_data['name'] + ", Email: " + user_data['email'] + ", Contact: +65" + user_data['phoneno'])

    return interested_buyers


def display_interested_buyers(property_id):
    interested_buyers = fetch_interested_buyers(property_id)

    # Create a new Toplevel window for displaying interested buyers
    buyers_window = tk.Toplevel(root)
    buyers_window.title("Interested Buyers")

    # Create a text widget to display interested buyers
    helvetica_font = ("Helvetica", 12)
    buyers_text = tk.Text(buyers_window, wrap=tk.NONE, font=helvetica_font)
    buyers_text.pack(fill=tk.BOTH, expand=True)

    # Display interested buyers in the new window
    for buyer in interested_buyers:
        buyers_text.insert(tk.END, f"{buyer}\n")


# Function to check if a user has already shown interest
def has_shown_interest(cursor, userid, property_id):
    query = f"SELECT COUNT(*) FROM Property_Buyer WHERE userid = ? AND property_id = ?"
    cursor.execute(query, (userid, property_id))
    count = cursor.fetchone()[0]
    return count > 0

# Function to add a new row in the Property_Buyer table
def add_interest(cursor, userid, property_id):
    query = "INSERT INTO Property_Buyer (userid, property_id) VALUES (?, ?)"
    cursor.execute(query, (userid, property_id))
    cursor.commit()


def show_interest(cursor, property_id):
    userid = check_user_id()  # You need to implement a function to get the current user's ID

    if not has_shown_interest(cursor, userid, property_id):
        add_interest(cursor, userid, property_id)
        messagebox.showinfo("Interest Shown", "You have successfully shown interest for this property.")
    else:
        messagebox.showinfo("Already Shown Interest", "You have already shown interest for this property.")



def show_user_info():
    # Connect to MongoDB
    client = MongoClient('localhost', 27017)
    db = client['DBMSProjectUsers']
    collection = db['collection_users']

    # Query MongoDB for the currently logged-in user
    userid = username_entry.get()
    user_document = collection.find_one({"userid": userid})

    if user_document:
        # Create a new window to display user information
        user_info_window = tk.Toplevel(root)
        user_info_window.title("User Information")

        edit_button = tk.Button(user_info_window, text="Edit", command=lambda: edit_user_info(user_document))
        edit_button.pack(side="right")

        # Display user information in the new window
        info_label = tk.Label(user_info_window, text=f"User Information\n\n"
                                                   f"User ID: {user_document['userid']}\n"
                                                   f"Name: {user_document['name']}\n"
                                                   f"Email: {user_document['email']}\n"
                                                   f"Phone Number: {user_document['phoneno']}",
                           font=('Arial', 12))
        info_label.pack(padx=10, pady=10)

    else:
        messagebox.showerror("Error", "User not found.")


def edit_user_info(user_document):
    # Create a new window for updating user information
    update_user_window = tk.Toplevel(root)
    update_user_window.title("Update User Information")

    # Create entry widgets to update user information
    name_label = tk.Label(update_user_window, text="Name:")
    name_label.pack()
    new_name_entry = tk.Entry(update_user_window)
    new_name_entry.insert(0, user_document['name'])
    new_name_entry.pack()

    email_label = tk.Label(update_user_window, text="Email:")
    email_label.pack()
    new_email_entry = tk.Entry(update_user_window)
    new_email_entry.insert(0, user_document['email'])
    new_email_entry.pack()

    phone_label = tk.Label(update_user_window, text="Phone Number:")
    phone_label.pack()
    new_phone_entry = tk.Entry(update_user_window)
    new_phone_entry.insert(0, user_document['phoneno'])
    new_phone_entry.pack()

    # Function to update user information in MongoDB
    def update_user_info():
        new_name = new_name_entry.get()
        new_email = new_email_entry.get()
        new_phone = new_phone_entry.get()

        client = MongoClient('localhost', 27017)
        db = client['DBMSProjectUsers']
        collection = db['collection_users']

        # Update the user information in MongoDB
        collection.update_one(
            {"userid": user_document['userid']},
            {"$set": {"name": new_name, "email": new_email, "phoneno": new_phone}}
        )

        # Show a success message
        messagebox.showinfo("Success", "User information updated successfully.")

        # Close the update_user_window
        update_user_window.destroy()

        # Update the information label in the main user_info_window
        tk.Label.config(text=f"User Information\n\n"
                               f"User ID: {user_document['userid']}\n"
                               f"Name: {new_name}\n"
                               f"Email: {new_email}\n"
                               f"Phone Number: {new_phone}")

    # Create a button to trigger the update
    update_button = tk.Button(update_user_window, text="Update Information", command=update_user_info)
    update_button.pack()


def add_user_window():
    # Create a new window for adding a user
    add_user_window = tk.Toplevel(root)
    add_user_window.title("Add User")

    # Create labels and entry widgets for user details
    user_details = ["userid", "password", "name", "email", "phoneno", "role"]

    entry_widgets = {}

    for i, detail in enumerate(user_details):
        label = tk.Label(add_user_window, text=f"{detail.capitalize()}:")
        label.grid(row=i, column=0, padx=10, pady=5, sticky="e")

        entry = tk.Entry(add_user_window)
        entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")

        entry_widgets[detail] = entry

    # Create a button to save the user details
    save_user_button = tk.Button(add_user_window, text="Save User", command=lambda: save_user(entry_widgets, add_user_window))
    save_user_button.grid(row=len(user_details), columnspan=2, pady=10)

def save_user(entry_widgets, add_user_window):
    # Retrieve the user details from the entry widgets
    user_data = {detail: entry.get() for detail, entry in entry_widgets.items()}

    # Validate the data (you can add more validation if needed)
    newuserid = next(iter(user_data.values()))

    # Insert the user data into the MongoDB collection
    insert_user_into_mongodb(user_data, add_user_window, newuserid)


def insert_user_into_mongodb(user_data, add_user_window, newuserid):
    try:
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['DBMSProjectUsers']
        collection = db['collection_users']

        # Insert the user data into the MongoDB collection
        collection.insert_one(user_data)

        # Close the add_user_window after successful insertion
        add_user_window.destroy()

        # Notify the admin that the user has been added
        messagebox.showinfo("Success", "User added successfully!")
        cursor = conn.cursor()
        log_user_action(check_user_id(), check_user_name(), "Added User: " + newuserid, cursor)

    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", "Failed to add user.")

    finally:
        # Close the database connection
        if 'conn' in locals() and conn:
            conn.close()


def delete_user_window():
    # Create a new window for deleting a user
    delete_user_window = tk.Toplevel(root)
    delete_user_window.title("Delete User")

    # Get the list of users from MongoDB
    user_list = get_user_list_from_mongodb()

    # Create a listbox to display the users
    user_listbox = tk.Listbox(delete_user_window, selectmode=tk.SINGLE)
    user_listbox.pack(pady=10)

    # Insert users into the listbox
    for user in user_list:
        user_listbox.insert(tk.END, user["userid"])

    # Create a button to delete the selected user
    delete_user_button = tk.Button(delete_user_window, text="Delete User",
                                   command=lambda: confirm_delete_user(user_listbox, delete_user_window))
    delete_user_button.pack(pady=10)


def confirm_delete_user(user_listbox, delete_user_window):
    # Get the selected user from the listbox
    selected_user_index = user_listbox.curselection()

    if selected_user_index:
        selected_user = user_listbox.get(selected_user_index)

        # Ask for confirmation
        response = messagebox.askokcancel("Confirm Deletion", f"Do you want to delete user: {selected_user}?")

        if response:
            # Delete the selected user from MongoDB
            delete_user_from_mongodb(selected_user)

            # Close the delete_user_window after successful deletion
            delete_user_window.destroy()


def delete_user_from_mongodb(useridtodel):
    try:
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['DBMSProjectUsers']
        collection = db['collection_users']

        # Delete the user from MongoDB
        collection.delete_one({"userid": useridtodel})

        # Notify the admin that the user has been deleted
        messagebox.showinfo("Success", f"User {useridtodel} deleted successfully!")
        cursor = conn.cursor()
        log_user_action(check_user_id(), check_user_name(), "Deleted User: " + useridtodel, cursor)

    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"Failed to delete user {useridtodel}.")

    finally:
        # Close the database connection
        if 'conn' in locals() and conn:
            conn.close()


def log_user_action(user_id, username, action_description,cursor):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        # Prepare the SQL query to insert the log
        query = "INSERT INTO AuditLog (userid, username, actions, timestamp) " \
                "VALUES (?, ?, ?, ?)"

        # Specify the values for the query
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Execute the query
        cursor.execute(query, user_id, username, action_description, timestamp)

        # Commit the transaction
        conn.commit()

    except Exception as e:
        print(f"Error logging user action: {e}")

    finally:
        # Close the database connection in the 'finally' block to ensure it's closed even if an exception occurs
        if 'conn' in locals() and conn:
            conn.close()


def show_audit_log():
    # Create a new window for displaying the audit log
    audit_log_window = tk.Toplevel(root)
    audit_log_window.title("Audit Log")

    try:
        cursor = conn.cursor()
        # Execute a query to retrieve audit log data
        cursor.execute('SELECT * FROM AuditLog')

        # Fetch all rows from the result set
        audit_log_data = cursor.fetchall()

        # Display the audit log data in the new window
        for row in audit_log_data:
            # Customize the display based on your needs
            # For example, create labels to show each column of the AuditLog table
            label = tk.Label(audit_log_window, text=f'UserID: {row.userid}, Name: {row.username}, Action: {row.actions}, Timestamp: {row.timestamp}')
            label.pack()

    except Exception as e:
        # Handle exceptions (e.g., database connection errors)
        print(f"Error: {e}")

    finally:
        # Close the database connection
        if 'conn' in locals() and conn:
            conn.close()


def logout(window):
    # Ask for confirmation before logging out
    confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if confirm:
        # Destroy the current window and return to the login screen
        window.destroy()
        reset_login_page()


def reset_login_page():
    # Show the main login window
    root.deiconify()

    # Clear the username and password entries
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    # Show the login widgets
    username_label.pack()
    username_entry.pack()
    password_label.pack()
    password_entry.pack()
    welcome_label.pack()
    login_button.pack()

    # Hide the search/filter frame
    search_frame.pack_forget()

    # Hide the background image
    background_label.pack()

    # Clear any existing search results in the result_text widget
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.config(state=tk.DISABLED)


# Create the main application window
root = tk.Tk()
root.title("Property Login Page")

# set resolution
root.geometry("1920x1080")

# Your existing code for background image and other widgets
# ...
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

# Modify the login_button command to call the new function
login_button = tk.Button(root, text="Login", command=validate_login_and_fetch_data)
login_button.pack()

# Your existing code for the search/filter bar and other widgets
# ...
# Create a frame for the search/filter bar
search_frame = tk.Frame(root)

# Create an entry field for search/filter
search_label = tk.Label()
#search_label.pack(side="left")

search_entry = tk.Entry()
#search_entry.pack(side="left")

search_button = tk.Button()
#search_button.pack(side="left")

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