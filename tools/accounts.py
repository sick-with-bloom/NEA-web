def generate_staff_code(staff_name):
    split_name = staff_name.split()
    first_name = split_name[0]
    surname = split_name[-1]
    staff_code = f"{first_name[0]}{surname[0]}{surname[-1]}".upper()
    return staff_code

def next_student_number():
    return None