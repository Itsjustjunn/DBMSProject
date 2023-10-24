import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
#
# # Import CSV Data
# # def get_data_csv():
# #     df = pd.read_csv("finaldata.csv")
# #     return df
# # df = get_data_csv()
#
# Function to validate the login credentials
def validate_login():
    username = username_entry.get()
    password = password_entry.get()

# Check if the username and password are correct (you can replace this with your own logic)
    if username == "sit" and password == "123":
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
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to perform the search or filter operation
def search_addresses():
    keyword = search_entry.get()
    result_listbox.delete(0, tk.END)
    for address in addresses:
        if keyword.lower() in address.lower():
            result_listbox.insert(tk.END, address)


# Sample list of addresses (replace with your actual data)
addresses = [
    "Jurong west",
    "woodlands",
    "tampines",
    # ...
]

# Create the main application window
root = tk.Tk()
root.title("Property Login Page")

# Load the background image using Pillow (PIL)
image = Image.open(r'C:\Users\chian\Downloads\Marina One Residences.jpg')
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
result_listbox = tk.Listbox(search_frame, font=('Arial', 20))
result_listbox.pack(side="left", fill="both", expand=True)

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
