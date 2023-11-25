from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['DBMSProjectUsers']

collection = db['collection_users']

collection.delete_many({})

doc_list = [
    {"userid": "sit", "password": "123", "name": "sit", "email": "sit@sit.edu.sg", "phoneno": "88888888", "role": "admin"},
    {"userid": "agent1", "password": "222", "name": "Dam", "email": "dam@somemail.edu.sg", "phoneno": "80800000", "role": "agent"},
    {"userid": "user1", "password": "456", "name": "Deez", "email": "deez@somemail.com", "phoneno": "80801111", "role": "buyer"},
    {"userid": "user2", "password": "789", "name": "Nutz", "email": "nutz@somemail.com", "phoneno": "80802222", "role": "buyer"},
]

collection.insert_many(doc_list)

cursor = collection.find({})
for document in cursor:
    print(document)