from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)
app.config["SECRET_KEY"] = ("your-secret-key-here")


@app.route("/")
def dashboard():
    #pull timetable data from db
    #populate dictionary
    #pass in as timetable
    return render_template("dashboard.html")

@app.route("/attendance")
def attendance():
    return render_template("attendance.html")

@app.route("/courses")
def courses():
    if session["logged_in"] != 1:
        return redirect(url_for("dashboard"))
    user = session["user"]
    from libraries.tools.admin import get_courses_by_staff_code, get_courses
    course_list = get_courses_by_staff_code(user)
    course_list = get_courses()
    return render_template("courses.html", course_list = course_list)

@app.route("/courses/<subject>")
def courses_subject():
    return

@app.route("/courses/<subject>/<year>")
def courses_subject_year():
    return

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
    from libraries.pages.register import register_page
    return register_page()

@app.route("/register/staff", methods = ["GET","POST"])
def register_staff():
    from libraries.pages.register import register_staff_page
    return register_staff_page()

@app.route("/register/student", methods = ["GET","POST"])
def register_student():
    from libraries.pages.register import register_student_page
    return register_student_page()

@app.route("/login", methods = ["GET", "POST"])
def login():
    from libraries.pages.login import login_page
    return login_page()

@app.route("/logout")
def logout():
    session["logged_in"] = 0
    session["user"] = None
    return redirect(url_for("dashboard"))


@app.before_request
def before_request():
    if "logged_in" not in session.keys():
        session["logged_in"] = 0

if __name__ == '__main__':
    app.run()
    session["logged_in"] = 0