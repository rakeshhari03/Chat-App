# 💬 Chat App

A real-time private chat application built using Django and Django Channels.

---

##  Tech Stack

- Python
- Django (MVT Architecture)
- Django Channels (WebSocket)
- SQLite
- HTML, CSS, JavaScript

---

## Features

- Custom User Model
- Register / Login / Logout
- Real-time 1-to-1 private chat
- Message persistence (saved in database)
- Read receipts (✓ / ✓✓)
- Typing indicator
- Online status tracking
- Prevent empty messages
- Authenticated WebSocket connections

---

## 🛠 Setup Instructions

### 1️⃣ Clone the Repository

git clone <your-repo-url>
cd chatapplication

### 2️⃣ Create a Virtual Environment

python -m venv env

Activate it:

Windows:
env\Scripts\activate


Mac/Linux:
source env/bin/activate

### 3️⃣ Install Dependencies
pip install django channels daphne


### 4️⃣ Apply Migrations
cd chat_app
python manage.py makemigrations
python manage.py migrate


---

## ▶️ Run the Project
python -m daphne chat_app.asgi:application

Because this project uses WebSockets, run using Daphne:


Open in browser:
http://127.0.0.1:8000/




---

##  Testing

1. Register two users  
2. Login from two browsers  
3. Start chat  
4. Verify:
   - ✓ when sent  
   - ✓✓ when read  
   - Typing indicator works  
\
---

##  Notes

- Uses InMemoryChannelLayer (development)
- Redis recommended for production

---

##  Developer

Rakesh Hari
