from flask import Flask, render_template, request, redirect, session, url_for
from routes.routes import routes  # Import Blueprint
from config.config import Config

app = Flask(__name__)
app.config.from_object(Config)  # Load configuration settings
app.secret_key = "your_secret_key"  # Needed for session management

# Register the Blueprint for user routes
app.register_blueprint(routes)

# --- User Authentication ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Example: Replace with actual database verification
        if username == "user" and password == "password":
            session["user_id"] = username
            session["is_admin"] = False  # Ensure user is not admin
            return redirect(url_for("routes.user_dashboard"))  # Redirect to user dashboard

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


# --- Admin Authentication ---
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Hardcoded admin credentials
        if username == "khawla" and password == "12345678":
            session["user_id"] = "admin"
            session["is_admin"] = True  # Set admin session
            return redirect(url_for("admin_dashboard"))

        return render_template("admin_login.html", error="Invalid credentials")

    return render_template("admin_login.html")


# --- Admin Dashboard ---
@app.route("/admin_dashboard")
def admin_dashboard():
    if not session.get("is_admin"):
        return redirect(url_for("login"))

    return render_template("admin_dashboard.html")


# --- Logout Route ---
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
