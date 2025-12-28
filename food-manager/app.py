from flask import Flask, render_template, request, redirect
from models.db import get_db

app = Flask(__name__)

LOCATIONS = [
    "Frigo Cucina",
    "Freezer Cucina",
    "Frigo Cantina",
    "Freezer Cantina",
    "Dispensa"
]

@app.route("/")
def home():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT id, name, location, quantity, expiry_date
        FROM foods
        WHERE expiry_date IS NOT NULL
        ORDER BY expiry_date ASC
        LIMIT 12
    """)
    foods = cur.fetchall()
    cur.close()
    db.close()
    return render_template("home.html", foods=foods, locations=LOCATIONS)

@app.route("/location/<name>")
def location(name):
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT id, name, quantity, expiry_date
        FROM foods
        WHERE location=%s
        ORDER BY name
    """, (name,))
    foods = cur.fetchall()
    cur.close()
    db.close()
    return render_template("location.html", foods=foods, location=name, locations=LOCATIONS)

@app.route("/add", methods=["POST"])
def add_food():
    data = request.form
    expiry = data["expiry_date"] if data["expiry_date"] else None

    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO foods (name, location, quantity, expiry_date)
        VALUES (%s, %s, %s, %s)
    """, (
        data["name"],
        data["location"],
        int(data.get("quantity", 1)),
        expiry
    ))
    db.commit()
    cur.close()
    db.close()
    return redirect("/")

@app.route("/consume/<int:id>")
def consume(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM foods WHERE id=%s", (id,))
    db.commit()
    cur.close()
    db.close()
    return redirect("/")
