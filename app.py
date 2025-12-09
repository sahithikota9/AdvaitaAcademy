from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
# Use an environment variable for production (Render). Fallback for local/dev.
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-please-change")

DATA_FILE = "students.json"

def load_students():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def find_student_by_username(username):
    students = load_students()
    for s in students:
        if s.get("username") == username:
            return s
    return None

@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        student = find_student_by_username(username)
        if student and student.get("password") == password:
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "danger")
            return render_template("login.html")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    student = find_student_by_username(username)
    if not student:
        flash("Student record not found.", "danger")
        return redirect(url_for("login"))

    # Ensure exams are newest-first
    exams = student.get("exams", [])
    exams_sorted = list(reversed(exams))

    # Compute totals/percentages if not present
    processed_exams = []
    for e in exams_sorted:
        s1 = e.get("math", None)
        s2 = e.get("physics", None)
        s3 = e.get("chemistry", None)

        # handle missing or null marks gracefully
        marks = []
        for m in (s1, s2, s3):
            try:
                marks.append(float(m))
            except Exception:
                marks.append(None)

        # compute total if possible
        if all(m is not None for m in marks):
            total = sum(marks)
            percentage = (total / (len(marks)*100)) * 100  # assuming each subject out of 100
        else:
            total = e.get("total", None)
            percentage = None

        processed_exams.append({
            "exam_name": e.get("exam_name", "Unnamed Exam"),
            "math": s1,
            "physics": s2,
            "chemistry": s3,
            "total": total,
            "percentage": round(percentage, 2) if percentage is not None else None,
            "notes": e.get("notes", "")
        })

    return render_template("dashboard.html",
                           student=student,
                           exams=processed_exams)

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    