# 🔐 Password Auditor & Secure Password Vault

A Python-based cybersecurity web application that evaluates password complexity and helps users securely manage their saved credentials through a password vault.

## 🚀 Features

- **Password Auditor:** Evaluates password complexity and identifies weak password practices.
- **User Authentication:** Login and signup pages for account access.
- **Dashboard:** Centralized interface for password auditing and vault management.
- **Secure Password Vault:** Manage stored credentials using a local SQLite database.
- **Database Models:** Organized data management using Python models.
- **Encryption Key Generation:** Utility for generating encryption keys.
- **Admin Interface:** Dedicated admin page for administrative functionality.
- **Web Interface:** HTML templates and CSS styling.

## 🛠️ Tech Stack

- **Language:** Python
- **Backend:** Python web application
- **Database:** SQLite
- **Database File:** `instance/vault.db`
- **Frontend:** HTML, CSS
- **Security:** Password auditing and credential protection
- **Dependencies:** See `requirements.txt`

## 📂 Project Structure

```text
Password-Auditor-Vault/
├── instance/
│   └── vault.db
├── static/
│   └── style.css
├── templates/
│   ├── admin.html
│   ├── dashboard.html
│   ├── login.html
│   └── signup.html
├── .env
├── app.py
├── generate_key.py
├── models.py
├── password_auditor.py
├── requirements.txt
├── vault.py
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/shahidshaikh-18/Password-Auditor-Vault.git
cd Password-Auditor-Vault
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

**Kali Linux / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Configure your local `.env` file with the environment variables required by your application.

**Security:** Never upload your `.env` file or private encryption keys to GitHub.

### 5. Run the application

```bash
python app.py
```

Open the local address displayed in your terminal.

## 🔍 Password Auditing

The password auditing module is intended to evaluate password characteristics such as:

- Password length
- Uppercase and lowercase letters
- Numeric characters
- Special characters
- Weak password patterns

The exact checks and strength classifications depend on the implementation in `password_auditor.py`.

## 🔒 Password Vault

The vault module is responsible for credential-management functionality. The application includes a local database file for storing application data.

For secure deployment, stored credentials should be protected using authenticated encryption, while account passwords should be hashed using a suitable password-hashing algorithm.

## 🧪 Testing

Recommended tests include:

- Checking weak and strong password examples.
- Testing signup and login validation.
- Verifying credential creation, retrieval, updating, and deletion.
- Checking that unauthorized users cannot access protected vault features.
- Confirming that sensitive information is not exposed in logs or error messages.

Use dummy credentials during testing.

## 🔮 Future Enhancements

- Compromised-password detection.
- Multi-factor authentication.
- Password generator.
- Password reuse detection.
- Security audit reports.
- Improved key management and vault protection.

## ⚠️ Disclaimer

This project is intended for educational and cybersecurity learning purposes. Review and test its security controls before storing real credentials.

## 👨‍💻 Author

**Shahid Shaikh**

Aspiring Cybersecurity Analyst | VAPT & Penetration Testing Enthusiast

