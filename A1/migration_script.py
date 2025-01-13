import psycopg2
from pymongo import MongoClient
from datetime import datetime, date

pg_conn = psycopg2.connect(
    dbname="universitydb",
    user="postgres",
    password="postgres",
    host="localhost"
)
pg_cursor = pg_conn.cursor()

mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["universitydb"]

def fetch_all(query):
    pg_cursor.execute(query)
    return pg_cursor.fetchall()

def convert_date_to_datetime(date_obj):
    if isinstance(date_obj, date):
        return datetime(date_obj.year, date_obj.month, date_obj.day)
    return date_obj


def migrate_students_with_enrollments():
    students = fetch_all("""
        SELECT s.*, d.department_name
        FROM Students s
        LEFT JOIN Departments d ON s.department_id = d.department_id
    """)
    
    enrollments = fetch_all("""
        SELECT e.enrollment_id, e.student_id, e.course_id, e.enrollment_date, e.grade, 
               c.course_name, c.course_code, c.credits, c.is_core, 
               i.first_name || ' ' || i.last_name AS instructor_name
        FROM Enrollments e
        JOIN Courses c ON e.course_id = c.course_id
        JOIN Instructors i ON c.instructor_id = i.instructor_id
    """)

    enrollment_map = {}
    for enroll in enrollments:
        student_id = enroll[1]
        if student_id not in enrollment_map:
            enrollment_map[student_id] = []
        enrollment_map[student_id].append({
            "course_id": enroll[2],
            "course_name": enroll[5],
            "course_code": enroll[6],
            "credits": enroll[7],
            "is_core": enroll[8],
            "instructor_name": enroll[9],  # Now refers to the correct index
            "enrollment_date": convert_date_to_datetime(enroll[3]),
            "grade": enroll[4]
        })

    student_docs = []
    for stu in students:
        student_docs.append({
            "_id": stu[0],
            "first_name": stu[1],
            "last_name": stu[2],
            "email": stu[3],
            "birth_date": convert_date_to_datetime(stu[4]),
            "enrollment_year": stu[5],
            "department": {
                "department_id": stu[6],
                "department_name": stu[7]
            },
            "enrollments": enrollment_map.get(stu[0], [])
        })

    mongo_db.students.insert_many(student_docs)


def migrate_courses_with_instructors():
    courses = fetch_all("""
        SELECT c.course_id, c.course_name, c.course_code, c.credits, c.is_core, 
               i.instructor_id, i.first_name || ' ' || i.last_name AS instructor_name, 
               d.department_id, d.department_name
        FROM Courses c
        LEFT JOIN Instructors i ON c.instructor_id = i.instructor_id
        LEFT JOIN Departments d ON c.department_id = d.department_id
    """)
    
    course_docs = []
    for course in courses:
        course_docs.append({
            "_id": course[0],  
            "course_name": course[1],  
            "course_code": course[2], 
            "credits": course[3],  
            "is_core": course[4],  
            "instructor": {
                "instructor_id": course[5],  
                "instructor_name": course[6] 
            },
            "department": {
                "department_id": course[7],  
                "department_name": course[8]  
            }
        })
    
    mongo_db.courses.insert_many(course_docs)


def migrate_instructors_with_departments():
    instructors = fetch_all("""
        SELECT i.*, d.department_name
        FROM Instructors i
        LEFT JOIN Departments d ON i.department_id = d.department_id
    """)
    
    instructor_docs = []
    for inst in instructors:
        instructor_docs.append({
            "_id": inst[0],
            "first_name": inst[1],
            "last_name": inst[2],
            "email": inst[3],
            "hire_date": convert_date_to_datetime(inst[4]),
            "department": {
                "department_id": inst[5],
                "department_name": inst[6]
            }
        })
    mongo_db.instructors.insert_many(instructor_docs)

migrate_students_with_enrollments()
migrate_courses_with_instructors()
migrate_instructors_with_departments()

pg_cursor.close()
pg_conn.close()
mongo_client.close()
