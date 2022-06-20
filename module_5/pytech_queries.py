from pymongo import MongoClient

url = "mongodb+srv://admin:admin@cluster0.8eh77vq.mongodb.net/pytech"

client = MongoClient(url)

db = client["pytech"]
collection = db["students"]

print("-- DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY --")
for x in collection.find():
    print("Student ID:" + x["student_id"])
    print("First Name:" + x["first_name"])
    print("Last Name:" + x["last_name"])
    print()

print("-- DISPLAYING STUDENT DOCUMENT FROM find_one() QUERY --")
col = collection.find_one({"student_id":"1008"})
print("Student ID:" + col["student_id"])
print("First Name:" + col["first_name"])
print("Last Name:" + col["last_name"])
