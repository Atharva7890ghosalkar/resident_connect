from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["Apartment"]
collection = db["residents"]

# Test if MongoDB is connected
print("✅ MongoDB Connected Successfully!")

# Fetch one record to verify connection
result = collection.find_one({"resident_name": "Atharva Ghosalkar"})
print(result)
