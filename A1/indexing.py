   
from pymongo import MongoClient

mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["universitydb"]   
   
def create_indexes():

    mongo_db.students.create_index([("student_id", 1)])
    
    mongo_db.courses.create_index([("course_id", 1)])
    mongo_db.courses.create_index([("course_id", 1), ("instructor_id", 1)]) 
    mongo_db.courses.create_index([("course_id", 1), ("department_id", 1)]) 
    

    mongo_db.instructors.create_index([("instructor_id", 1)])
    mongo_db.instructors.create_index([("instructor_id", 1), ("department_id", 1)])  

create_indexes()

print("Indexes created successfully!")

mongo_client.close()