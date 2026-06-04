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