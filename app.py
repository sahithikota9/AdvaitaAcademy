from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Load students
with open("students.json") as f:
    students = json.load(f)

# Load results
with open("results.json") as f:
    results = json.load(f)


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def do_login():
    username = request.form["username"]
    password = request.form["password"]

    # Check if student exists and password matches
    if username in students and students[username]["password"] == password:
        session["username"] = username
        return redirect("/dashboard")

    return "Invalid username or password"


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")

    username = session["username"]
    student = students.get(username)
    student_results = results.get(username, [])

    # Calculate totals for each exam
    for exam in student_results:
        exam["total"] = exam["math"] + exam["physics"] + exam["chemistry"]

    return render_template("dashboard.html", student=student, results=student_results)


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)