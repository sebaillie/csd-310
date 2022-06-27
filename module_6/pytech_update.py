from pymongo import MongoClient

url = "mongodb+srv://admin:admin@cluster0.8eh77vq.mongodb.net/pytech"

client = MongoClient(url)

db = client["pytech"]
collection = db["students"]

studentSearch = '1007'
studentNewLastName = 'Werbenmanjensen'

# Call the find() method and output the documents to the terminal window
print("-- DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY --")
for values in collection.find():
    print("Student ID: " + values["student_id"])
    print("First Name: " + values["first_name"])
    print("Last Name: " + values["last_name"])
    print()

# Call the update_one method by student_id 1007 and update the last name to something different than the originally saved name
collection.update_one( { 'student_id' : studentSearch }, { "$set": { 'last_name' : studentNewLastName } } )

# Call the find_one method by student_id 1007 and output the document to the terminal window
print("\n-- DISPLAYING STUDENT DOCUMENT " + studentSearch + " --")
value = collection.find_one( { 'student_id' : studentSearch } )
print("Student ID: " + value["student_id"])
print("First Name: " + value["first_name"])
print("Last Name: " + value["last_name"])
print("\n\n")

input("End of program, press any key to continue...")
