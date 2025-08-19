# 🏨 The Grand Retreat — Hotel & Event Booking System

A modern Django-based hotel and event booking web app. Guests can browse rooms, view details, and make bookings with check-in and check-out dates. Admins can manage rooms and users can manage their profiles.

![Made with Django](https://img.shields.io/badge/Made%20with-Django-0C4B33.svg?style=for-the-badge&logo=django)
---

## 🚀 Features

- 🧾 User registration & login
- 🛏️ View rooms and detailed info
- 📅 Book rooms (check-in/check-out)
- 📦 Admin room management
- 📧 Contact form for inquiries
- 🖼️ Room detail page with booking modal
- 🧑 User profile with image upload
- 🔐 Authentication protected views
- 🎨 Responsive Bootstrap 5 interface

---

## 🛠️ Tech Stack

| Layer       | Technology     |
|-------------|----------------|
| Backend     | Django 5.x     |
| Frontend    | HTML, CSS (Bootstrap 5), JS |
| Database    | SQLite (default) |
| Auth        | Django Auth    |
| Styling     | Bootstrap 5    |

---

## 📁 Project Structure

mainproject/
├── main/ # Home, contact, profile views
├── rooms/ # Room & booking logic
├── events/ # Event showcase
├── templates/ # HTML templates
├── static/ # Static files (CSS, JS)
├── media/ # Uploaded media
├── db.sqlite3 # SQLite database
└── manage.py


---

## ⚙️ Getting Started

### 1. Clone the Repository

git clone https://github.com/YOUR_USERNAME/the-grand-retreat.git

cd the-grand-retreat

2. Set Up Virtual Environment
python -m venv env
# Activate
env\Scripts\activate   
# Windows
source env/bin/activate    
# macOS/Linux

3. Install Dependencies
pip install -r requirements.txt


If you don’t have requirements.txt, install Django manually:

pip install django

4. Run Migrations
python manage.py makemigrations
python manage.py migrate

5. Create Superuser
python manage.py createsuperuser

6. Run the Development Server
python manage.py runserver


Open your browser at: http://127.0.0.1:8000


👤 Admin Panel Access

After creating the superuser, visit:

http://127.0.0.1:8000/admin/

🧪 Example Test User (optional)
Username	Password	Role
siddhu	    123   	Admin


🙌 Credits

Bootstrap 5

Django Framework

Pexels for free images


🌐 Future Improvements (Optional Ideas)

Online payment integration (Razorpay, Stripe, etc.)

Booking calendar for availability

Admin approval of bookings

Event ticketing system

Built with ❤️ using Django

