from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from email_validator import validate_email, EmailNotValidError

author = Blueprint("author", __name__)

@author.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = current_app.al.hush_hush(request.form.get("password"), email)
        print(email, password)

        if not email:
            return render_template("login.html", error = "Fill email adress.")
        
        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError as e:
            return render_template("login.html", error = "Not valid email adress.")
        
        if not password:
            return render_template("login.html", error = "Wrong password.")

        al = current_app.al
        #koukni do DB jestli je email registrovany
        if al.login(email, password):
            session["email"] = email
            print("logged in")
            return redirect(url_for("views.home"))
        else:
            print("not found")
            return render_template("login.html", error="Wrong email or password.")
       
    return render_template("login.html", error = "")

@author.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get("email")
        password1 = current_app.al.hush_hush(request.form.get("password1"), email)
        password2 = current_app.al.hush_hush(request.form.get("password2"), email)
        print(password1, password2)

        if not email:
            return render_template("signup.html", error = "Not valid email adress.")
        # try:
        #     valid = validate_email(email)
        #     email = valid.email
        # except EmailNotValidError as e:
        #     return render_template("signup.html", error="Not valid email adress.")
            
        if password1 != password2:
            return render_template("signup.html", error = "Passwords do not match.")

        # SaveToDB(email,password)
        al = current_app.al
        if al.register(email, password1):
            session["email"] = email
            return redirect(url_for("views.home"))
        else:
            print("not found")
            return render_template("signup.html", error="email already used")
       
    return render_template("signup.html", error = "")