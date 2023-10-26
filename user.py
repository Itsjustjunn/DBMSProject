import json

def getUserInfo(json_file, userID):
    try:
        with open(json_file, 'r') as file:
            user_data = json.load(file)

            if userID in user_data:
                user_info = user_data[userID]
                return User(userID, user_info['username'], user_info['email'])
            else:
                return None

    except FileNotFoundError:
        print("JSON file not found")
        return None
    except Exception as e:
        print(f"Error fetching user info: {e}")
        return None

def editUser(json_file, UserID, user):
    try:
        with open(json_file, 'r') as file:
            user_data = json.load(file)

        if UserID in user_data:
            user_data[UserID]['username'] = user.username
            user_data[UserID]['email'] = user.email

            with open(json_file, 'w') as file:
                json.dump(user_data, file, indent=4)

            print("User information updated successfully")
        else:
            print("User not found")

    except FileNotFoundError:
        print("JSON file not found")






import json

# Function to load the database from a JSON file
def load_database(filename):
    try:
        with open(filename, "r") as infile:
            database = json.load(infile)
        return database
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        return []

# Function to save the database to a JSON file
def save_database(filename, database):
    with open(filename, "w") as outfile:
        json.dump(database, outfile, indent=4)

# Function to add a new record to the database
def add_record(database, new_record):
    database.append(new_record)
    return database

# Function to retrieve user info by name
def get_user_info(database, name):
    for record in database:
        if record["name"] == name:
            return record
    return None

# Function to edit user info by name
def edit_user_info(database, name, new_info):
    for record in database:
        if record["name"] == name:
            record.update(new_info)
            return True
    return False

# Function to print all records
def print_records(database):
    for record in database:
        print("Name:", record["name"])
        print("Age:", record["age"])
        print("Email:", record["email"])
        print()

# Main program
def main():
    filename = "database.json"
    database = load_database(filename)

    while True:
        print("1. Add a new record")
        print("2. Get user info by name")
        print("3. Edit user info by name")
        print("4. Print all records")
        print("5. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            email = input("Enter email: ")
            new_record = {
                "name": name,
                "age": age,
                "email": email
            }
            database = add_record(database, new_record)
            save_database(filename, database)
            print("Record added.\n")
        elif choice == "2":
            name = input("Enter name to retrieve user info: ")
            user_info = get_user_info(database, name)
            if user_info:
                print("User Info:")
                print("Name:", user_info["name"])
                print("Age:", user_info["age"])
                print("Email:", user_info["email"])
            else:
                print("User not found.")
        elif choice == "3":
            name = input("Enter name to edit user info: ")
            new_info = {}
            new_info["name"] = input("Enter new name: ")
            new_info["age"] = int(input("Enter new age: "))
            new_info["email"] = input("Enter new email: ")
            if edit_user_info(database, name, new_info):
                save_database(filename, database)
                print("User info edited.")
            else:
                print("User not found.")
        elif choice == "4":
            print("Records in the database:\n")
            print_records(database)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


