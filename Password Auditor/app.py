from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, VaultEntry
from vault import vault_bp
import os

app = Flask(__name__)
app.secret_key = "change-this-later"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vault.db"
db.init_app(app)
app.register_blueprint(vault_bp)


# Sign-up page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template(
                "signup.html",
                message="Username already exists. Try logging in instead.",
            )

        new_user = User(
            username=username, password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        return render_template(
            "signup.html",
            message=f"Account created for {username}! You can now log in.",
        )

    return render_template("signup.html")


# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session["username"] = username
            return redirect(url_for("vault_bp.dashboard"))
        else:
            return render_template(
                "login.html", message="Invalid username or password."
            )

    return render_template("login.html")


# Admin viewer - see all users and all vault entries (for learning/debugging only)
@app.route("/admin")
def admin_viewer():
    if "username" not in session:
        return redirect(url_for("login"))

    all_users = User.query.all()
    all_entries = VaultEntry.query.all()

    # Vault passwords are encrypted (reversible), so we decrypt them for viewing
    from vault import cipher

    decrypted_entries = []
    for entry in all_entries:
        decrypted_entries.append(
            {
                "username": entry.username,
                "site": entry.site,
                "site_username": entry.site_username,
                "password": cipher.decrypt(entry.encrypted_password.encode()).decode(),
            }
        )

    return render_template("admin.html", users=all_users, entries=decrypted_entries)


# Home page -> redirect to signup
@app.route("/")
def home():
    return redirect(url_for("signup"))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
