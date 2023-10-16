#import pandas to data clean / format the datasets
import pandas as pd
from IPython.display import display


#reading the unclean dataset


df = pd.read_csv('ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv', index_col=[0])
print(df)

# Create a dictionary with the data for the new row
#new_row = {'Name': 'David', 'Age': 40}
#new_row = {'month': '2025-01', 'town': 'LA', 'flat_type':'Mansion','block':'30','street_name':'Beverly Hills',	'storey_range':'1',	'floor_area_sqm':'5000sqm',	'flat_model':'New',	'lease_commence_date':'2015','remaining_lease':'freehold','resale_price':'53000000'}

# Append the dictionary to the DataFrame
#df = df.append(new_row, ignore_index=True)

# Reset the index
#df = df.reset_index(drop=True)

print(df)