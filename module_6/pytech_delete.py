# https://github.com/sebaillie/csd-310/blob/main/module_6/pytech_delete.py
from pymongo import MongoClient

url = "mongodb+srv://admin:admin@cluster0.8eh77vq.mongodb.net/pytech"

client = MongoClient(url)

db = client["pytech"]
collection = db["students"]

john = {
    "student_id" : "1010",
    "first_name" : "John",
    "last_name" : "Doe"
}

# Call the find() method and output the documents to the terminal window
print("-- DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY --")
for values in collection.find():
    print("Student ID: " + values["student_id"])
    print("First Name: " + values["first_name"])
    print("Last Name: " + values["last_name"])
    print()

# Call the insert_one() method
print("-- INSERT STATEMENTS --")
student = collection.insert_one(john)
print("Inserted student record into the students collection with document_id " + str(student.inserted_id) + "\n")

# Call find_one() method to get new record
print("-- DISPLAYING STUDENT TEST DOC --")
value = collection.find_one( { 'student_id' : '1010' } )
print("Student ID: " + value["student_id"])
print("First Name: " + value["first_name"])
print("Last Name: " + value["last_name"])
print()

# Call delete_one() method for student 1010
collection.delete_one( { 'student_id' : '1010' } )

# Call the find() method and output the documents to the terminal window
print("-- DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY --")
for values in collection.find():
    print("Student ID: " + values["student_id"])
    print("First Name: " + values["first_name"])
    print("Last Name: " + values["last_name"])
    print()


input("End of program, press any key to continue...")
