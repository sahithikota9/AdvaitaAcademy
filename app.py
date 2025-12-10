from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = "secret123"   # change later if needed


# --------- LOAD DATA ---------

def load_students():
    with open("students.json", "r") as f:
        return json.load(f)

def load_results():
    with open("results.json", "r") as f:
        return json.load(f)


# --------- ROUTES ---------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        students = load_students()

        # Check username exists
        if username in students and students[username]["password"] == password:
            session["username"] = username
            return redirect("/dashboard")

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")

    username = session["username"]

    students = load_students()
    results = load_results()

    student = students[username]

    # Get this student's exams
    exam_list = results.get(username, [])

    # Sort newest → oldest (your requirement)
    exam_list = list(reversed(exam_list))

    # Add total marks automatically
    for exam in exam_list:
        exam["total"] = exam["math"] + exam["physics"] + exam["chemistry"]

    # Chart data
    exam_names = [exam["exam"] for exam in exam_list]
    totals = [exam["total"] for exam in exam_list]

    return render_template(
        "dashboard.html",
        name=student["name"],
        roll=student["roll"],
        results=exam_list,
        exam_names=exam_names,
        totals=totals
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# --------- RUN LOCALLY ---------
if __name__ == "__main__":
    app.run(debug=True)
