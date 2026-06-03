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

@app.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("name")
        password = request.form.get("password")
        account_type = request.form.get("type")
        if account_type == "Staff":
            from tools.accounts import generate_staff_code
            staff_code = generate_staff_code(name)
            print(staff_code)
        elif account_type == "Student":
            from tools.accounts import next_student_number
            student_number
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