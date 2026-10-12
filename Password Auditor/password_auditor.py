import re
import hashlib
import requests

# Check Password Length
def check_length(password):
    if len(password) < 8:
        return False, "Password is too short (minimum 8 characters)"
    return True, "Length OK"

#  Check Password Complexity
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


password = input("Enter a password to audit: ")

length_ok, length_msg = check_length(password)
complexity_ok, complexity_msg = check_complexity(password)

print(f"\nLength Check: {length_msg}")
print(f"Complexity Check: {complexity_msg}")

# Breach-Check Function
def check_pwned(password):
    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")

    if response.status_code != 200:
        return False, "Could not check breach database (no internet or API error)"

    hashes = response.text.splitlines()
    for line in hashes:
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return True, f"Password found in {count} known data breaches!"

    return False, "Password not found in known breaches"

pwned_found, pwned_msg = check_pwned(password)
print(f"Breach Check: {pwned_msg}")