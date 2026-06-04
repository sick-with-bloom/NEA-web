from flask import Flask, render_template, session, redirect, url_for, request

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
    if request.method == "GET":
        if session["logged_in"] != 0:
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html")
    else:
        username = request.form.get("username").upper()
        password = request.form.get("password")
        account_information = [username, password, 0]

        if len(username) == 3:
            #staff login
            print("staff login")
            account_information[2] = 1
        elif len(username) == 8:
            #student login
            print("student login")
            account_information[2] = 2
        else:
            #incorrect username
            print("incorrect username")
            return render_template("login.html")

        from libraries.tools.accounts import login

        if login(account_information):
            session["logged_in"] = account_information[2]
            print(f"logged in as {username}")
            return render_template("dashboard.html")
        else:
            print("login failed")
            return render_template("login.html")


@app.route("/logout")
def logout():
    session["logged_in"] = 0
    return redirect(url_for("dashboard"))

if __name__ == '__main__':
    app.run()