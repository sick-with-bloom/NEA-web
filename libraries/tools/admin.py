def generate_staff_code(staff_name):
    split_name = staff_name.split()
    first_name = split_name[0]
    surname = split_name[-1]
    staff_code = f"{first_name[0]}{surname[0]}{surname[-1]}".upper()
    return staff_code

def generate_next_student_number(year):
    start_year = str(year)[-2:]

    from libraries.tools.database import execute_query_one

    query = ("SELECT student_number "
             "FROM student "
             "WHERE student_number like CONCAT(?,'%') "
             "ORDER BY student_number DESC")
    last_student_number = execute_query_one(query, (start_year,))
    if last_student_number:
        last_student_number = last_student_number[0]
        last_student_number_int = int(last_student_number[3:])
        next_student_number_int = last_student_number_int + 1
        next_student_number = f"S{start_year}{str(next_student_number_int).zfill(5)}"
    else:
        next_student_number = f"S{start_year}00001"
    return next_student_number

def add_new_student(student_information):
    student_name = student_information[0]
    split_name = student_name.split()
    surname = split_name[-1]
    other_names = " ".join(split_name[:-1])
    student_date_of_birth = student_information[1]
    student_password = student_information[2]

    start_year = calculate_start_year(student_date_of_birth)
    student_number = generate_next_student_number(start_year)

    from libraries.tools.database import execute_query_add
    from libraries.tools.utils import hash_password

    query = "INSERT INTO student (student_number, surname, other_names, date_of_birth) VALUES (?, ?, ?, ?)"
    params = (student_number, surname, other_names, student_date_of_birth, )
    execute_query_add(query, params)

    query = "INSERT INTO student_login (student_number, password) VALUES (?, ?)"
    params = (student_number, hash_password(student_password),)
    execute_query_add(query, params)

def calculate_start_year(date_of_birth):
    birth_year = int(date_of_birth[:4])
    start_year = birth_year + 16
    print(start_year)
    return start_year

def add_new_staff_member(staff_information):
    staff_name = staff_information[0]
    split_name = staff_name.split()
    first_name = split_name[0]
    surname = split_name[-1]
    other_names = " ".join(split_name[:-1])
    staff_code = f"{first_name[0]}{surname[0]}{surname[-1]}".upper()
    department_id = staff_information[1]
    staff_password = staff_information[2]

    from libraries.tools.database import execute_query_add
    from libraries.tools.utils import hash_password

    query = "INSERT INTO staff (staff_code, surname, other_names, department_id) VALUES (?, ?, ?, ?)"
    params = (staff_code, surname, other_names, department_id, )
    execute_query_add(query, params)

    query = "INSERT INTO staff_login (staff_code, password) VALUES (?, ?)"
    params = (staff_code, hash_password(staff_password),)
    execute_query_add(query, params)

def login(account_information):
    username = account_information[0]
    password = account_information[1]
    account_type = account_information[2]

    from libraries.tools.database import execute_query_one
    from libraries.tools.utils import hash_password

    if account_type == 1:
        query = "SELECT staff_code FROM staff_login WHERE staff_code = ? and password = ?"
    elif account_type == 2:
        query = "SELECT student_number FROM student_login WHERE student_number = ? and password = ?"
    else:
        print("invalid account type")
        return False

    success = execute_query_one(query, (username, hash_password(password)))

    if success:
        return True
    else:
        return False

def get_subjects_by_staff_code(staff_code):
    from libraries.tools.database import execute_query_all
    query = ("SELECT subject_id, subject_name FROM subject, staff "
             "WHERE subject.department_id = staff.department_id "
             "AND staff.staff_code = ?")
    subjects = execute_query_all(query, (staff_code, ))
    return subjects

def get_courses():
    from libraries.tools.database import execute_query_all
    query = ("SELECT course.course_id, subject.subject_name, course.year "
             "FROM subject, course "
             "WHERE course.subject_id = subject.subject_id")
    courses = execute_query_all(query, ())
    return courses

def get_courses_by_staff_code(staff_code):
    from libraries.tools.database import execute_query_all
    query = ("SELECT subject.subject_name, course.year "
             "FROM staff, department, subject, course "
             "WHERE staff.staff_code = ? "
             "AND staff.department_id = department.department_id "
             "AND department.department_id = subject.department_id "
             "AND course.subject_id = subject.subject_id")
    courses = execute_query_all(query, (staff_code, ))
    return courses

def get_courses_by_subject_id(subject_id):
    from libraries.tools.database import execute_query_all
    query = ("SELECT subject.subject_name, course.year "
             "FROM course, subject "
             "WHERE course.subject_id = subject.subject_id "
             "AND subject.subject_id = ?")
    courses = execute_query_all(query, (subject_id, ))
    return courses

def get_courses_by_subject_id_and_year(subject_id, year):
    from libraries.tools.database import execute_query_all
    query = ("SELECT subject.subject_name, course.year "
             "FROM course, subject "
             "WHERE course.subject_id = subject.subject_id "
             "AND subject.subject_id = ? "
             "AND course.year = ?")
    courses = execute_query_all(query, (subject_id, year, ))
    return courses

def get_classes_by_course(course_id):
    from libraries.tools.database import execute_query_all
    query = ("SELECT subject.subject_name, class.block, course.year, teaching.staff_code "
             "FROM class, course, subject, teaching, staff "
             "WHERE class.course_id = course.course_id "
             "AND course.subject_id = subject.subject_id "
             "AND course.course_id = ? "
             "AND class.class_id = teaching.class_id ")
    classes = execute_query_all(query, (course_id, ))
    return classes

def get_students_by_course(course_id):
    from libraries.tools.database import execute_query_all
    query = ("SELECT * FROM student, enrolment, class "
             "WHERE student.student_number = enrolment.student_number "
             "AND enrolment.class_id = class.class_id "
             "AND class.course_id = ?")
    students = execute_query_all(query, (course_id, ))
    return students

def add_new_class(class_information):
    from libraries.tools.database import execute_query_add, execute_query_one
    block = class_information[0]
    course_id = class_information[1]
    room_number = class_information[2]
    staff_code = class_information[3]
    print(class_information)

    #need to check if there is already a class in the desired room for the desired block
    query = ("SELECT * FROM room_booking, class "
             "WHERE room_booking.room_number = ? "
             "AND class.block = ?")
    existing_booking = execute_query_one(query, (room_number, block, ))
    if existing_booking:
        return False

    #need to check if there is already a class assigned to the teacher for the desired block
    query = ("SELECT * FROM teaching, class "
             "WHERE teaching.staff_code = ? "
             "AND teaching.class_id = class.class_id "
             "AND class.block = ?")
    existing_teaching = execute_query_one(query, (staff_code, block, ))
    if existing_teaching:
        return False

    query = ("INSERT INTO class (block, course_id) "
             "VALUES (?, ?)")
    execute_query_add(query, (block, course_id, ))

    query = "SELECT class_id FROM class ORDER BY class_id DESC"
    class_id = execute_query_one(query, ())[0]

    query = ("INSERT INTO room_booking (room_number, class_id) "
             "VALUES (?, ?)")
    execute_query_add(query, (room_number, class_id, ))

    query = ("INSERT INTO teaching (staff_code, class_id) "
             "VALUES (?, ?)")
    print(staff_code, class_id)
    execute_query_add(query, (staff_code, class_id, ))

    return True

def get_rooms_by_course_id(course_id):
    from libraries.tools.database import  execute_query_all
    query = ("SELECT * FROM room, department, course, subject "
             "WHERE room.department_id = department.department_id "
             "AND course.subject_id = subject.subject_id "
             "AND subject.department_id = department.department_id "
             "AND course.course_id = ?")
    rooms = execute_query_all(query, (course_id, ))
    return rooms

def get_rooms():
    from libraries.tools.database import execute_query_all
    query = ("SELECT room_number, department_name FROM room, department "
             "WHERE room.department_id = department.department_id")
    rooms = execute_query_all(query, ())
    return rooms

def get_rooms_by_department(department_id):
    from libraries.tools.database import execute_query_all
    query = ("SELECT room_number, department_name FROM room, department "
             "WHERE room.department_id = department.department_id "
             "AND department.department_id = ?")
    rooms = execute_query_all(query, (department_id,))
    return rooms

def get_departments():
    from libraries.tools.database import execute_query_all
    query = "SELECT * FROM department"
    departments = execute_query_all(query, ())
    return departments

def get_staff_by_course_id(course_id):
    from libraries.tools.database import execute_query_all
    query = ("SELECT staff.staff_code, staff.surname, staff.other_names FROM staff "
             "JOIN subject ON staff.department_id = subject.department_id "
             "JOIN course ON course.subject_id = subject.subject_id "
             "WHERE course.course_id = ?")
    staff = execute_query_all(query, (course_id, ))
    return staff
