# 📝 Employee Survey Web Application

This is a Flask-based web application that allows employees to submit feedback through a survey form. Admin users can register, log in, view responses, edit or delete submissions, and log out securely.

---

## 🚀 Features

- ✅ User registration and login
- ✅ Survey form submission
- ✅ View submitted survey
- ✅ Edit and delete responses
- ✅ Auto-redirect to home after submission
- ✅ Session-based authentication
- ✅ SQLite database integration

---

## 🛠️ Technologies Used

- Python 3.x
- Flask
- Jinja2
- Flask SQLAlchemy
- Flask Login
- HTML5 & CSS3
- SQLite

---

## 📁 Project Structure

```
employee_survey/
│
├── app.py                # Main Flask application
├── survey.db             # SQLite database file
├── models.py             # SQLAlchemy models (User, Survey)
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── survey.html
│   ├── edit.html
│   └── thankyou.html
├── static/               # CSS / JS / images if needed
│   └── style.css
└── README.md             # Project overview
```

---

## 💾 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/employee_survey.git
cd employee_survey
```

### 2. Create and activate a virtual environment (optional but recommended)

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# OR
source venv/bin/activate  # On macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not created yet, install manually:

```bash
pip install flask flask_sqlalchemy flask_login
```

### 4. Run the application

```bash
python app.py
```

Then open your browser and navigate to:

```
http://localhost:5000
```

---

## 🧪 Demo

- Register a new user
- Login and fill the survey
- Edit or delete your survey
- Logout securely

---

## 🔐 Login Credentials

Once registered, your credentials will be stored in `survey.db` securely with hashed passwords using Flask-Login.

---

## 📌 Notes

- The app uses **SQLite**, which stores all data in `survey.db`
- For production, consider switching to PostgreSQL/MySQL and using environment variables for secrets

---

---

## ✅ Conclusion

This Employee Survey Web App provides a simple yet functional platform for collecting, managing, and updating employee feedback. Built with Flask and SQLite, it's ideal for small teams or educational projects looking to understand web development fundamentals, form handling, and session management. Future improvements could include user roles, data analytics, and deployment on cloud platforms.


