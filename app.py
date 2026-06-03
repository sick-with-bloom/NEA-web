from flask import Flask, render_template, session, redirect, url_for, request
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = ("your-secret-key-here")

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/attendance")
def attendance():
    return render_template("attendance.html")

@app.route("/students")
def students():
    return render_template("students.html")

@app.route("/reports")
def reports():
    return render_template("reports.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/timetable")
def timetable():
    return render_template("timetable.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register/staff", methods = ["GET","POST"])
def register_staff():
    if request.method == "GET":
        from tools.database import execute_query_all
        departments = execute_query_all("SELECT * FROM department", ())
        return render_template("register_staff.html", departments=departments)
    else:
        name = request.form.get("name")
        password = request.form.get("password")
        department_id = request.form.get("department")
        from tools.accounts import generate_staff_code, add_new_staff_member
        staff_code = generate_staff_code(name)
        add_new_staff_member([
            staff_code,
            name,
            pa
        ])
        return redirect(url_for("dashboard"))

@app.route("/register/student", methods = ["GET","POST"])
def register_student():
    if request.method == "GET":
        return render_template("register_student.html")
    else:
        name = request.form.get("name")
        password = request.form.get("password")
        from tools.accounts import calculate_start_year, generate_next_student_number, add_new_student
        start_year = calculate_start_year(request.form.get("date_of_birth"))
        student_number = generate_next_student_number(start_year)
        student_information = [
            request.form.get("name"),
            request.form.get("date_of_birth"),
            student_number,
            request.form.get("password")
        ]
        add_new_student(student_information)
        return redirect(url_for("dashboard"))

@app.route("/staff_login")
def staff_login():
    session["logged_in"] = 1
    return redirect(url_for("dashboard"))
    #return render_template("staff_login.html")

@app.route("/student_login")
def student_login():
    session["logged_in"] = 2
    return redirect(url_for("dashboard"))
    #return render_template("student_login.html")

@app.route("/login")
def login():
    session["logged_in"] = True
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session["logged_in"] = 0
    return redirect(url_for("dashboard"))

if __name__ == '__main__':
    app.run()