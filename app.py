from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Load students
with open("students.json") as f:
    students = json.load(f)

# Load results
with open("results.json") as f:
    results = json.load(f)


# -------------- LOGIN PAGE --------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check username + password
        if username in students and students[username]["password"] == password:
            session["username"] = username
            return redirect("/dashboard")

        # If login fails:
        return render_template("login.html", error="Invalid username or password")

    # GET request → show login page
    return render_template("login.html")



# -------------- DASHBOARD PAGE --------------
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")

    username = session["username"]
    student = students.get(username)
    student_results = results.get(username, [])

    # Add total marks into the data
    for exam in student_results:
        exam["total"] = exam["math"] + exam["physics"] + exam["chemistry"]

    return render_template("dashboard.html", student=student, results=student_results)



# -------------- LOGOUT --------------
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")



# -------------- RUN APP (local only) --------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)