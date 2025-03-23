# routes/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models.models import get_db_connection

# Create Blueprint
routes = Blueprint("routes", __name__)

# Middleware for login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("routes.login"))
        return f(*args, **kwargs)
    return decorated_function

# Register Route
@routes.route("/")
def index():
    conn = get_db_connection()
    cars = conn.execute("SELECT * FROM cars WHERE available = 1").fetchall()
    conn.close()
    return render_template("index.html", cars=cars)

@routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        # Check if username already exists
        existing_user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if existing_user:
            conn.close()
            return "Username already exists. Please choose a different one."  # Inform the user properly
        
        try:
            # If username does not exist, insert the new user
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for("routes.login"))  # Redirect to login page after successful registration
        except Exception as e:
            conn.close()
            return f"An error occurred: {e}"

    return render_template("register.html")

@routes.route("/login", methods=["GET", "POST"])
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
            return redirect(url_for("routes.admin_dashboard") if user["is_admin"] == 1 else url_for("routes.index"))
        return "Invalid username or password"  # Error message for wrong credentials
    return render_template("login.html")

@routes.route("/car/<int:car_id>")
def car_details(car_id):
    conn = get_db_connection()
    car = conn.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()
    conn.close()
    if car is None:
        abort(404)
    return render_template("car_details.html", car=car)

@routes.route("/logout")
@login_required
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("is_admin", None)
    return redirect(url_for("routes.index"))

@routes.route("/admin")
@login_required
def admin_dashboard():
    conn = get_db_connection()
    cars = conn.execute("SELECT * FROM cars").fetchall()
    conn.close()
    return render_template("admin_dashboard.html", cars=cars)

@routes.route("/admin/add_car", methods=["POST"])
@login_required
def add_car():
    brand = request.form["brand"]
    model = request.form["model"]
    space = request.form["space"]
    speed = request.form["speed"]
    color = request.form["color"]
    image = request.form["image"]
    price = request.form["price"]

    conn = get_db_connection()
    conn.execute("INSERT INTO cars (brand, model, space, speed, color, image, price) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                 (brand, model, space, speed, color, image, price))
    conn.commit()
    conn.close()

    return redirect(url_for("routes.admin_dashboard"))

@routes.route("/admin/delete_car/<int:car_id>")
@login_required
def delete_car(car_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM cars WHERE id = ?", (car_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("routes.admin_dashboard"))

@routes.route("/admin/toggle_availability/<int:car_id>")
@login_required
def toggle_availability(car_id):
    conn = get_db_connection()
    car = conn.execute("SELECT available FROM cars WHERE id = ?", (car_id,)).fetchone()
    if car:
        new_availability = 1 if car["available"] == 0 else 0
        conn.execute("UPDATE cars SET available = ? WHERE id = ?", (new_availability, car_id))
        conn.commit()
    conn.close()
    return redirect(url_for("routes.admin_dashboard"))

@routes.route("/admin/edit_car/<int:car_id>")
@login_required
def edit_car(car_id):
    conn = get_db_connection()
    car = conn.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()
    conn.close()
    if car is None:
        abort(404)
    return render_template("edit_car.html", car=car)

@routes.route("/admin/update_car/<int:car_id>", methods=["POST"])
@login_required
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
    return redirect(url_for("routes.admin_dashboard"))

@routes.route("/car/<int:car_id>/reserve", methods=["POST"])
@login_required
def reserve_car(car_id):
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    user_id = session["user_id"]

    conn = get_db_connection()
    conn.execute("INSERT INTO reservations (user_id, car_id, start_date, end_date) VALUES (?, ?, ?, ?)", 
                 (user_id, car_id, start_date, end_date))
    conn.commit()
    conn.close()

    return redirect(url_for("routes.index"))

@routes.route("/reservations")
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

# Add routes for reviews here:
@routes.route("/car/<int:car_id>/review", methods=["POST"])
@login_required
def add_review(car_id):
    rating = request.form["rating"]
    comment = request.form["comment"]
    user_id = session["user_id"]

    conn = get_db_connection()
    conn.execute("INSERT INTO reviews (user_id, car_id, rating, comment) VALUES (?, ?, ?, ?)", 
                 (user_id, car_id, rating, comment))
    conn.commit()
    conn.close()
    return redirect(url_for("routes.car_details", car_id=car_id))

@routes.route("/admin/reviews")
@login_required
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

@routes.route("/admin/respond_review/<int:review_id>", methods=["POST"])
@login_required
def respond_review(review_id):
    response = request.form["response"]
    conn = get_db_connection()
    conn.execute("UPDATE reviews SET admin_response = ? WHERE id = ?", (response, review_id))
    conn.commit()
    conn.close()
    return redirect(url_for("routes.admin_reviews"))
