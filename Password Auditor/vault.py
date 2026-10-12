from flask import Blueprint, request, render_template, redirect, url_for, session
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from models import db, VaultEntry
import os
import re
import hashlib
import requests

load_dotenv()

vault_bp = Blueprint("vault_bp", __name__)

encryption_key = os.environ.get("ENCRYPTION_KEY")
cipher = Fernet(encryption_key.encode())


# Password strength/breach check functions
def check_length(password):
    if len(password) < 8:
        return False, "Too short (minimum 8 characters)"
    return True, "Length OK"


def check_complexity(password):
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"[0-9]", password))
    has_symbol = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))

    missing = []
    if not has_upper:
        missing.append("uppercase letter")
    if not has_lower:
        missing.append("lowercase letter")
    if not has_digit:
        missing.append("number")
    if not has_symbol:
        missing.append("special character")

    if missing:
        return False, f"Missing: {', '.join(missing)}"
    return True, "Complexity OK"


def check_pwned(password):
    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    if response.status_code != 200:
        return False, "Could not check breach database"

    for line in response.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return True, f"Found in {count} known data breaches!"

    return False, "Not found in known breaches"


# Dashboard route
@vault_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    check_result = None

    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "check_password":
            password = request.form.get("check_password_input")
            length_ok, length_msg = check_length(password)
            complexity_ok, complexity_msg = check_complexity(password)
            pwned_found, pwned_msg = check_pwned(password)

            check_result = {
                "length_msg": length_msg,
                "complexity_msg": complexity_msg,
                "pwned_msg": pwned_msg,
            }

        elif form_type == "add_entry":
            site = request.form.get("site")
            site_username = request.form.get("site_username")
            site_password = request.form.get("site_password")

            encrypted_password = cipher.encrypt(site_password.encode()).decode()

            new_entry = VaultEntry(
                username=username,
                site=site,
                site_username=site_username,
                encrypted_password=encrypted_password,
            )
            db.session.add(new_entry)
            db.session.commit()

    # Get only this user's entries from the database, decrypt for display
    user_entries = VaultEntry.query.filter_by(username=username).all()
    entries = []
    for entry in user_entries:
        decrypted = cipher.decrypt(entry.encrypted_password.encode()).decode()
        entries.append({
            "id": entry.id,
            "site": entry.site,
            "site_username": entry.site_username,
            "password": decrypted,
        })

    return render_template("dashboard.html", entries=entries, check_result=check_result)


# Delete a vault entry
@vault_bp.route("/vault/delete/<int:entry_id>", methods=["POST"])
def delete_entry(entry_id):
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    entry = VaultEntry.query.filter_by(id=entry_id, username=username).first()

    if entry:
        db.session.delete(entry)
        db.session.commit()

    return redirect(url_for("vault_bp.dashboard"))