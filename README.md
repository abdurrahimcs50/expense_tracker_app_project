````markdown
# 💸 Expense Tracker Web App

A robust Django-powered personal finance manager built with Python, MySQL, Bootstrap, and Chart.js — designed to give users clear insights and effortless control over their expenses.

---

## 🚀 Features

- User Registration & Login with secure sessions  
- Add, edit, and delete expenses  
- Categorize expenses for smarter tracking  
- Filter by date, category, or amount for detailed views  
- Dynamic expense summary charts powered by Chart.js  
- Export expense data to CSV for offline use  
- Fully responsive UI built with Bootstrap 5  

---

## 🛠️ Tech Stack

- **Backend:** Django, Python  
- **Frontend:** HTML, CSS, Bootstrap 5, Chart.js  
- **Database:** MySQL  
- **Authentication:** Django sessions  
- **Deployment:** Any WSGI-compatible server (Gunicorn + Nginx recommended)

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/abdurrahimcs50/expense_tracker_app_project.git
cd expense_tracker_app_project
````

### 2. Create and activate a virtual environment

```bash
python3 -m venv env
source env/bin/activate    # On Windows: env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL database

* Create a MySQL database and user
* Update your `settings.py` with database credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (optional, for admin access)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser to see the app in action.

---

## 📈 Deployment Notes

For production:

* Use Gunicorn as WSGI server
* Use Nginx as a reverse proxy
* Configure HTTPS (e.g., via Let's Encrypt)
* Set `DEBUG = False` in `settings.py`
* Use environment variables for sensitive data

---

## 📝 License

This project is licensed under the MIT License.

---

If you want me to help with Docker setup, CI/CD, or adding tests, just say the word!
