from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# 🟢 Home Page - Choose Role
@app.route("/")
def index():
    return render_template("index.html")


# 🟢 Driver Signup
@app.route("/driver_signup", methods=["GET", "POST"])
def driver_signup():
    if request.method == "POST":
        file = request.files["license"]
        if file:
            filename = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filename)

            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (role, license_image) VALUES (?, ?)", ("driver", file.filename))
            conn.commit()
            conn.close()

            return redirect("/driver_settings")
    return render_template("driver_signup.html")


# 🟢 Driver Settings Page
@app.route("/driver_settings")
def driver_settings():
    return render_template("driver_settings.html")


# 🟢 Route Suggestions Page
@app.route("/route")
def route():
    return render_template("route.html")


# 🟢 Upload Dog Sighting Report
@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        file = request.files["dogImage"]
        description = request.form["description"]
        lat = request.form["latitude"]
        lng = request.form["longitude"]

        if file:
            filename = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filename)

            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO reports (user_id, image, description, latitude, longitude) VALUES (?, ?, ?, ?, ?)",
                (1, file.filename, description, lat, lng),
            )
            conn.commit()
            conn.close()

        return redirect("/")
    return render_template("report.html")


# 🟢 Authority Signup
@app.route("/authority_signup", methods=["GET", "POST"])
def authority_signup():
    if request.method == "POST":
        position = request.form["position"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (role, position) VALUES (?, ?)", ("authority", position))
        conn.commit()
        conn.close()

        return redirect("/authority_dashboard")
    return render_template("authority_signup.html")


# 🟢 Authority Dashboard - View Reports
@app.route("/authority_dashboard")
def authority_dashboard():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports")
    reports = cursor.fetchall()
    conn.close()

    return render_template("authority_dashboard.html", reports=reports)


# 🟢 API Endpoint: Get Danger Zones (For JavaScript to use)
@app.route("/get_zones")
def get_zones():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM danger_zones")
    zones = cursor.fetchall()
    conn.close()

    return jsonify(zones)


if __name__ == "__main__":
    app.run(debug=True)
