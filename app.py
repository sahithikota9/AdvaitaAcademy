from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# --- Load JSON files ---
def load_students():
    with open("students.json", "r") as f:
        return json.load(f)

def load_results():
    with open("results.json", "r") as f:
        return json.load(f)

students = load_students()
results = load_results()

# ---------------- LOGIN PAGE -----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in students and students[username]["password"] == password:
            session["username"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# ---------------- DASHBOARD -----------------
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")

    username = session["username"]
    student = students[username]
    exams = results.get(username, [])

    # SORT newest → oldest for display
    exams_sorted = sorted(exams, key=lambda x: x["exam"], reverse=True)

    # For the line chart: oldest → newest
    exams_old_first = exams_sorted[::-1]

    exam_names = [e["exam"] for e in exams_old_first]
    exam_totals = [
        e["math"] + e["physics"] + e["chemistry"] 
        for e in exams_old_first
    ]

    return render_template(
        "dashboard.html",
        name=student["name"],
        username=username,
        roll=student["roll"],
        exams=exams_sorted,
        exam_names=exam_names,
        exam_totals=exam_totals
    )

# ---------------- LOGOUT -----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- RUN -----------------
if __name__ == "__main__":
    app.run(debug=True)
