from pymongo import MongoClient

url = "mongodb+srv://admin:admin@cluster0.8eh77vq.mongodb.net/pytech"

client = MongoClient(url)

db = client["pytech"]
collection = db["students"]

thorin = {
    "student_id" : "1007",
    "first_name" : "Thorin",
    "last_name" : "Oakenshield"
}

bilbo = {
    "student_id" : "1008",
    "first_name" : "Bilbo",
    "last_name" : "Baggins"
}

frodo = {
    "student_id" : "1009",
    "first_name" : "Frodo",
    "last_name" : "Baggins"
}
 
student1 = collection.insert_one(thorin)
student2 = collection.insert_one(bilbo)
student3 = collection.insert_one(frodo)

print("-- INSERT STATEMENTS --")
print("Inserted student record " + thorin["first_name"] + " " + thorin["last_name"] + "into the students collection with document_id " + str(student1.inserted_id))
print("Inserted student record " + bilbo["first_name"] + " " + bilbo["last_name"] + "into the students collection with document_id " + str(student2.inserted_id))
print("Inserted student record " + frodo["first_name"] + " " + frodo["last_name"] + "into the students collection with document_id " + str(student3.inserted_id))
