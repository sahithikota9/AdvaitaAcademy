from flask import Flask, render_template, request, redirect, url_for
import json
import re

app = Flask(__name__)

# ---------------------------
# Load students
# ---------------------------
with open("students.json", "r") as f:
    students = json.load(f)

# ---------------------------
# Load results
# ---------------------------
with open("results.json", "r") as f:
    results = json.load(f)


# ---------------------------
# Helper: extract exam number
# ---------------------------
def get_exam_number(exam_name):
    """
    Extracts the exam number from strings like:
    'JEE Mock Test 1'
    'JEE Mock Test 12'
    """
    num = re.findall(r"\d+", exam_name)
    return int(num[-1]) if num else 0


# ---------------------------
# LOGIN PAGE
# ---------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in students and students[username]["password"] == password:
            return redirect(url_for("dashboard", username=username))

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


# ---------------------------
# DASHBOARD PAGE
# ---------------------------
@app.route("/dashboard/<username>")
def dashboard(username):
    student = students.get(username)
    exam_list = results.get(username, [])

    # ---- Calculate totals ----
    for exam in exam_list:
        exam["total"] = exam["math"] + exam["physics"] + exam["chemistry"]

    # ---- Sorting using extracted exam number ----
    exams_for_graph = sorted(exam_list, key=lambda x: get_exam_number(x["exam"]))
    exams_for_display = sorted(exam_list, key=lambda x: get_exam_number(x["exam"]), reverse=True)

    graph_labels = [e["exam"] for e in exams_for_graph]
    graph_totals = [e["total"] for e in exams_for_graph]

    return render_template(
        "dashboard.html",
        student=student,
        exams=exams_for_display,
        graph_labels=graph_labels,
        graph_totals=graph_totals
    )


# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
