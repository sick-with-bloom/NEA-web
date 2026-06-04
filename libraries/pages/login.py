def login_page():
    from flask import request, session, render_template, redirect, url_for
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
            return redirect(url_for("dashboard"))
        else:
            print("login failed")
            return render_template("login.html")