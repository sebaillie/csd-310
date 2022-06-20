from pymongo import MongoClient

url = "mongodb+srv://admin:admin@cluster0.8eh77vq.mongodb.net/pytech"

client = MongoClient(url)

db = client["pytech"]

print("-- PyTech Collection List --")
print(db.list_collection_names())
