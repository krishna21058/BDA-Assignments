
CREATE TABLE Departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Instructors (
    instructor_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL, 
    last_name VARCHAR(100) NOT NULL,  
    email VARCHAR(150) UNIQUE NOT NULL,
    hire_date DATE CHECK (hire_date <= CURRENT_DATE), 
    department_id INT,
    CONSTRAINT fk_instructor_department FOREIGN KEY(department_id) REFERENCES Departments(department_id) ON DELETE SET NULL 
);

CREATE TABLE Students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL, 
    last_name VARCHAR(100) NOT NULL,   
    email VARCHAR(150) UNIQUE NOT NULL,
    birth_date DATE CHECK (birth_date <= CURRENT_DATE), 
    enrollment_year INT CHECK (enrollment_year >= 1900 AND enrollment_year <= EXTRACT(YEAR FROM CURRENT_DATE)), 
    department_id INT,
    CONSTRAINT fk_department FOREIGN KEY(department_id) REFERENCES Departments(department_id) ON DELETE SET NULL  
);

CREATE TABLE Courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(50) UNIQUE NOT NULL,
    credits INT NOT NULL CHECK (credits > 0 AND credits <= 10),  
    is_core BOOLEAN DEFAULT FALSE,  
    department_id INT,
    instructor_id INT,
    CONSTRAINT fk_course_department FOREIGN KEY(department_id) REFERENCES Departments(department_id) ON DELETE CASCADE
);

CREATE TABLE Enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT,
    course_id INT,
    enrollment_date DATE NOT NULL CHECK (enrollment_date <= CURRENT_DATE),  
    grade VARCHAR(2) CHECK (grade IS NULL OR grade IN ('A', 'A-', 'B-', 'B', 'C', 'D', 'F', 'I', 'W')), 
    CONSTRAINT fk_enrollment_student FOREIGN KEY(student_id) REFERENCES Students(student_id) ON DELETE CASCADE, 
    CONSTRAINT fk_enrollment_course FOREIGN KEY(course_id) REFERENCES Courses(course_id) ON DELETE CASCADE  
);

CREATE TABLE CourseInstructor (
    course_id INT,
    instructor_id INT,
    year_offered INT NOT NULL CHECK (year_offered >= 1900 AND year_offered <= EXTRACT(YEAR FROM CURRENT_DATE)),  
    CONSTRAINT fk_course_instructor_course FOREIGN KEY(course_id) REFERENCES Courses(course_id) ON DELETE CASCADE, 
    CONSTRAINT fk_course_instructor_instructor FOREIGN KEY(instructor_id) REFERENCES Instructors(instructor_id) ON DELETE CASCADE, 
    PRIMARY KEY (course_id, instructor_id,year_offered)
);
