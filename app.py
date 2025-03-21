from flask import Flask, render_template, request, redirect, url_for, session, abort
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from database import create_database

app = Flask(__name__)
app.secret_key = "your_secret_key"

def get_db_connection():
    conn = sqlite3.connect("database/car_rental.db")
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None or session.get("is_admin") != 1:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    conn = get_db_connection()
    cars = conn.execute("SELECT * FROM cars WHERE available = 1").fetchall()
    conn.close()
    return render_template("index.html", cars=cars)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["is_admin"] = user["is_admin"]
            if user["is_admin"] == 1:
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("index"))
        else:
            return "Invalid username or password"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return "Username already exists"
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("is_admin", None)
    return redirect(url_for("index"))

@app.route("/admin")
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    cars = conn.execute("SELECT * FROM cars").fetchall()
    conn.close()
    return render_template("admin_dashboard.html", cars=cars)

@app.route("/car/<int:car_id>")
def car_details(car_id):
    conn = get_db_connection()
    car = conn.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()
    conn.close()
    if car is None:
        abort(404)
    return render_template("car_details.html", car=car)

@app.route("/car/<int:car_id>/reserve", methods=["POST"])
@login_required
def reserve_car(car_id):
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    user_id = session["user_id"]

    conn = get_db_connection()
    conn.execute("INSERT INTO reservations (user_id, car_id, start_date, end_date) VALUES (?, ?, ?, ?)", (user_id, car_id, start_date, end_date))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/reservations")
@login_required
def user_reservations():
    user_id = session["user_id"]
    conn = get_db_connection()
    reservations = conn.execute("""
        SELECT cars.brand, cars.model, reservations.start_date, reservations.end_date
        FROM reservations
        JOIN cars ON reservations.car_id = cars.id
        WHERE reservations.user_id = ?
    """, (user_id,)).fetchall()
    conn.close()
    return render_template("user_reservations.html", reservations=reservations)

@app.route("/admin/add_car", methods=["POST"])
@admin_required
def add_car():
    brand = request.form["brand"]
    model = request.form["model"]
    space = request.form["space"]
    speed = request.form["speed"]
    color = request.form["color"]
    image = request.form["image"]
    price = request.form["price"]

    conn = get_db_connection()
    conn.execute("INSERT INTO cars (brand, model, space, speed, color, image, price) VALUES (?, ?, ?, ?, ?, ?, ?)", (brand, model, space, speed, color, image, price))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete_car/<int:car_id>")
@admin_required
def delete_car(car_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM cars WHERE id = ?", (car_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/toggle_availability/<int:carid>")
@admin_required
def toggle_availability(car_id):
    conn = get_db_connection()
    car = conn.execute("SELECT available FROM cars WHERE id = ?", (car_id,)).fetchone()
    if car:
        new_availability = 1 if car["available"] == 0 else 0
        conn.execute("UPDATE cars SET available = ? WHERE id = ?", (new_availability, car_id))
        conn.commit()
    conn.close()
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/edit_car/<int:car_id>")
@admin_required
def edit_car(car_id):
    conn = get_db_connection()
    car = conn.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()
    conn.close()
    if car is None:
        abort(404)
    return render_template("edit_car.html", car=car)

@app.route("/admin/update_car/<int:car_id>", methods=["POST"])
@admin_required
def update_car(car_id):
    brand = request.form["brand"]
    model = request.form["model"]
    space = request.form["space"]
    speed = request.form["speed"]
    color = request.form["color"]
    image = request.form["image"]
    price = request.form["price"]

    conn = get_db_connection()
    conn.execute("""
        UPDATE cars
        SET brand = ?, model = ?, space = ?, speed = ?, color = ?, image = ?, price = ?
        WHERE id = ?
    """, (brand, model, space, speed, color, image, price, car_id))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_dashboard"))

# Add routes for reviews here:
@app.route("/car/<int:car_id>/review", methods=["POST"])
@login_required
def add_review(car_id):
    rating = request.form["rating"]
    comment = request.form["comment"]
    user_id = session["user_id"]

    conn = get_db_connection()
    conn.execute("INSERT INTO reviews (user_id, car_id, rating, comment) VALUES (?, ?, ?, ?)", (user_id, car_id, rating, comment))
    conn.commit()
    conn.close()
    return redirect(url_for("car_details", car_id=car_id))

@app.route("/admin/reviews")
@admin_required
def admin_reviews():
    conn = get_db_connection()
    reviews = conn.execute("""
        SELECT reviews.*, users.username, cars.brand, cars.model
        FROM reviews
        JOIN users ON reviews.user_id = users.id
        JOIN cars ON reviews.car_id = cars.id
    """).fetchall()
    conn.close()
    return render_template("admin_reviews.html", reviews=reviews)

@app.route("/admin/respond_review/<int:review_id>", methods=["POST"])
@admin_required
def respond_review(review_id):
    response = request.form["response"]
    conn = get_db_connection()
    conn.execute("UPDATE reviews SET admin_response = ? WHERE id = ?", (response, review_id))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_reviews"))

if __name__ == "__main__":
    create_database()
    app.run(debug=True)