# 🚗 Car Wash Booking System (Django)

A simple Django-based web application for booking car wash services and managing them through staff and admin dashboards.
---

## 📌 Features
* User can book car wash
* Check car wash status using car number
* Staff dashboard to manage bookings
* Admin panel for full control
---

## ⚙️ Installation
1. Clone the repository
```
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. Create virtual environment
```
python -m venv env
```

3. Activate environment
```
env\Scripts\activate
```

4. Install dependencies
```
pip install -r requirements.txt
```

5. Run migrations
```
python manage.py migrate
```

6. Create superuser
```
python manage.py createsuperuser
```

7. Run server
```
python manage.py runserver
```

---
## 🌐 Access URLs
After running the server, open:

 👤 User Interface
```
http://127.0.0.1:8000/
```
* Book car wash
* Check car status
---

 🔐 Admin Panel (Superuser)
```
http://127.0.0.1:8000/admin
```
* Full control of database
* Manage all records
---

 👨‍🔧 Staff Dashboard
```
http://127.0.0.1:8000/admin-dashboard
```
* View bookings
* Update status (Processing, Washing, Completed, Collected)
---

 🛠 Tech Stack
* Python
* Django
* HTML, CSS, JavaScript
---

 📌 Notes
* Make sure server is running before accessing URLs
* Use superuser credentials to access admin panel
* Staff dashboard is for internal use
---
