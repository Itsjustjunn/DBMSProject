#def getUserInfo(string userID):
    try:
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
      
        query = "SELECT * FROM users WHERE user_id = ?"
        cursor.execute(query, (userID,))
        
        user_info = cursor.fetchone()

        if user_info:
            return user_id
        else:
            return None 

#editUser(string UserID, User user)
 try:
    
        conn = sqlite3.connect('database')
        cursor = conn.cursor()
   
        query = "UPDATE users SET username = ?, email = ? WHERE user_id = ?"
        cursor.execute(query, (user.username, user.email, UserID))
        
        conn.commit()
   
        if cursor.rowcount == 0:
            print("User not found")
        else:
            print("User information updated successfully")

    except sqlite3.Error as e:
        print(f"Error editing user info: {e}")

    finally:
        conn.close()

