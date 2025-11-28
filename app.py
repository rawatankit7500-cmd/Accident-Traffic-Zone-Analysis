from flask import Flask, render_template, request, redirect, session
import pandas as pd
import folium
from folium.plugins import HeatMap
import sqlite3
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Database create if not exists
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- Home ----------
@app.route('/')
def home():
    return render_template("index.html")

# ---------- Signup ----------
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == "POST":
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users(username, password) VALUES (?,?)", (username, password))
            conn.commit()
        except:
            conn.close()
            return "Username already exists. Try another."
        conn.close()
        return redirect('/login')

    return render_template("signup.html")

# ---------- Login ----------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = username
            return redirect('/search')
        else:
            return "Invalid username or password. Try again."

    return render_template("login.html")

# ---------- Search ----------
@app.route('/search', methods=['GET','POST'])
def search():
    if "user" not in session:
        return redirect('/login')

    if request.method == "POST":
        area = request.form['area']
        return redirect(f"/result/{area}")

    return render_template("search.html")

# ---------- Result + Charts + Heatmap ----------
@app.route('/result/<area>')
def result(area):
    df = pd.read_csv("accidents_in_dehradun.csv")
    df['Area'] = df['Area'].str.title()

    area_coords = {
        "Prem Nagar": [30.3141, 77.9700],
        "Clock Tower": [30.3245, 78.0412],
        "Vikas Nagar": [30.4700, 77.7800],
        "Rajpur Road": [30.3643, 78.0746],
        "Race Course": [30.3080, 78.0435],
        "Ballupur": [30.3205, 78.0185],
        "Isbt": [30.2742, 78.0088]
    }

    if area.title() not in area_coords:
        return "Area not found. Try: Prem Nagar, ISBT, Rajpur Road etc."

    area_data = df[df['Area'] == area.title()]

    # ---------- MAP ----------
    m = folium.Map(location=area_coords[area.title()], zoom_start=14)

    # Accident markers
    for _, row in area_data.iterrows():
        sev = row['Severity'].lower()
        color = "red" if sev == "high" else "orange" if sev == "medium" else "green"

        folium.CircleMarker(
            location=area_coords[area.title()],
            radius=6,
            popup=f"{row['Vehicle_Type']} | {row['Accident_Cause']} | {row['Severity']}",
            color=color,
            fill=True,
        ).add_to(m)

    # ---------- HEATMAP ----------
    heat_list = [area_coords[area.title()]] * len(area_data)
    HeatMap(heat_list).add_to(m)

    map_file = f"static/{area}.html"
    m.save(map_file)

    # ---------- PIE CHART (Severity) ----------
    severity_counts = area_data['Severity'].value_counts()
    plt.figure(figsize=(5,5))
    severity_counts.plot(kind='pie', autopct='%1.0f%%')
    plt.title("Severity Distribution")
    pie_chart = f"static/{area}_pie.png"
    plt.savefig(pie_chart)
    plt.close()

    # ---------- BAR CHART (Vehicle Type) ----------
    vehicle_counts = area_data['Vehicle_Type'].value_counts()
    plt.figure(figsize=(6,4))
    vehicle_counts.plot(kind='bar')
    plt.title("Accidents by Vehicle Type")
    plt.xlabel("Vehicle Type")
    plt.ylabel("Count")
    bar_chart = f"static/{area}_bar.png"
    plt.savefig(bar_chart)
    plt.close()

    return render_template("results.html",
                           area=area.title(),
                           map_file=map_file,
                           pie_chart=pie_chart,
                           bar_chart=bar_chart)

# ---------- Logout ----------
@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect('/')

app.run(debug=True)
