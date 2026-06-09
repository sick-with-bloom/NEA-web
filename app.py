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

@app.route("/courses", methods = ["POST","GET"])
def courses():
    if request.method == "GET":
        if session["logged_in"] != 1:
            return redirect(url_for("dashboard"))
        user = session["user"]
        from libraries.tools.admin import get_courses_by_staff_code, get_courses
        course_list = get_courses_by_staff_code(user)
        course_list = get_courses()
        return render_template("course_list.html", course_list = course_list)
    else:
        from libraries.tools.admin import get_classes_by_course
        course_id = request.form.get("course_id")
        redirect_url = f"/courses/id={course_id}"
        return redirect(redirect_url)
        #return redirect(url_for("dashboard"))

@app.route("/rooms", methods=["GET","POST"])
def rooms():
    if request.method == "GET":
        from libraries.tools.admin import get_rooms, get_departments
        room_list = get_rooms()
        department_list = get_departments()
        return render_template("room_list.html", room_list = room_list, department_list = department_list)
    else:
        department_id = request.form.get("department")
        return redirect(f"/rooms/department_id={department_id}")
    #return redirect(url_for("dashboard"))

@app.route("/rooms/department_id=<department_id>",  methods=["GET","POST"])
def rooms_by_department(department_id):
    if request.method == "GET":
        from libraries.tools.admin import get_rooms_by_department, get_departments
        room_list = get_rooms_by_department(department_id)
        department_list = get_departments()
        return render_template("room_list.html", room_list=room_list, department_list=department_list)
    else:
        department_id = request.form.get("department")
        return redirect(f"/rooms/department_id={department_id}")


@app.route("/classes/new/course=<course_id>", methods=["GET","POST"])
def new_class(course_id):
    if request.method == "GET":
        from libraries.tools.admin import get_rooms_by_course_id
        rooms = get_rooms_by_course_id(course_id)
        return render_template("class_new.html", course_id = course_id, rooms = rooms)
    else:
        block = request.form.get("block")
        room = request.form.get("room")

        from libraries.tools.admin import add_new_class

        add_new_class([block, course_id, room])

        redirect_url = f"/courses/id={course_id}"
        return redirect(redirect_url)

@app.route("/courses/subject=<subject_id>" ,methods = ["POST","GET"])
def courses_subject(subject_id):
    from libraries.tools.admin import get_courses_by_subject_id
    course_list = get_courses_by_subject_id(subject_id)
    return render_template("course_list.html", course_list = course_list)

@app.route("/courses/subject=<subject_id>/year=<year>", methods = ["POST","GET"])
def courses_subject_year(subject_id, year):
    from libraries.tools.admin import get_courses_by_subject_id_and_year
    course_list = get_courses_by_subject_id_and_year(subject_id, year)
    return render_template("course_list.html", course_list=course_list)

@app.route("/courses/id=<course_id>")
def course(course_id):
    from libraries.tools.admin import get_classes_by_course, get_students_by_course
    class_list = get_classes_by_course(course_id)
    student_list = get_students_by_course(course_id)
    return render_template("course.html", class_list=class_list, student_list=student_list, course_id = course_id)

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