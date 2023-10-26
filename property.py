import sqlite3
import string

database = "database.db"


#reading the unclean dataset


df = pd.read_csv('ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv', index_col=[0])
print(df)


# getAllProperties
def getallproperties():
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Property")
        properties = cursor.fetchall()
        conn.close()

        if properties:
            return properties
        else:
            return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def getproperty(propertyID):
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Properties WHERE propertyID = ?", (propertyID,))
        property_data = cursor.fetchone()  # Fetch one row
        conn.close()

        if property_data:
            property_id, property_name, property_location, property_price = property_data
            return {
                "propertyID": property_id,
                "propertyName": property_name,
                "propertyLocation": property_location,
                "propertyPrice": property_price
                # Add more properties as needed, TO BE CHANGED ACCORDING TO DATABASE
            }
        else:
            return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# addProperty(Property property)
# editProperty(string propertyID, Property property)
def deleteproperty(propertyID):
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Properties WHERE propertyID = ?", (propertyID,))
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        conn.rollback()  # Rollback the transaction in case of an error
        conn.close()
# indicateInterest(userID, propertyID)
# viewInterestedBuyers(propertyID)