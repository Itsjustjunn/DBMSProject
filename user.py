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


