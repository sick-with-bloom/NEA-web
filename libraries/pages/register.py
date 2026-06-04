def register_page():
    from flask import render_template
    return render_template("register.html")

def register_staff_page():
    from flask import request, render_template, redirect, url_for
    if request.method == "GET":
        from libraries.tools.database import execute_query_all
        departments = execute_query_all("SELECT * FROM department", ())
        return render_template("register_staff.html", departments=departments)
    else:
        name = request.form.get("name")
        password = request.form.get("password")
        department_id = request.form.get("department")
        from libraries.tools.accounts import generate_staff_code, add_new_staff_member
        staff_code = generate_staff_code(name)
        add_new_staff_member([
            request.form.get("name"),
            request.form.get("department"),
            request.form.get("password")
        ])
        return redirect(url_for("dashboard"))

def register_student_page():
    from flask import request, render_template, redirect, url_for
    if request.method == "GET":
        return render_template("register_student.html")
    else:
        from libraries.tools.accounts import add_new_student
        student_information = [
            request.form.get("name"),
            request.form.get("date_of_birth"),
            request.form.get("password")
        ]
        add_new_student(student_information)
        return redirect(url_for("dashboard"))