Career Predictor & Daily Task Tracker (Flask + ML)

A Flask-based web application that predicts a user’s career using a Machine Learning model and provides daily task-based roadmaps to help users achieve their career goals.
The project includes login/signup with email or phone, user progress tracking, and personalized daily plans.

🚀 Features

🔐 Login / Signup System

Single input for Email or Phone

Prevents duplicate signup

Stores user name and identifier

🤖 Career Prediction

Machine Learning model (model.pkl)

Predicts career based on:

Subjects

Work Style

Career Goal

Education

🗺️ Career Roadmaps

Step-by-step career guidance

📅 Daily Task Planner

Career-specific daily tasks

Progress saved per user

“Mark as Completed” functionality

💾 SQLite Database

User data

Daily progress tracking

⚙️ Session Management

User-specific data using Flask sessions

🛠️ Tech Stack

Backend: Python, Flask

Frontend: HTML, CSS

Database: SQLite

Machine Learning: Scikit-learn (Pickle model)

Tools: VS Code, Git, GitHub

📂 Project Structure
career_predictor2/
│
├── app.py
├── model.pkl
├── users.db
├── requirements.txt
│
├── templates/
│   ├── login.html
│   ├── index.html
│   ├── roadmap.html
│   ├── daily_plan.html
│
├── static/
│   └── style.css
│
└── README.md

🗄️ Database Schema
Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    phone TEXT UNIQUE
);

Progress Table
CREATE TABLE progress (
    user_id INTEGER,
    career TEXT,
    day INTEGER,
    PRIMARY KEY (user_id, career)
);

▶️ How to Run the Project

Clone the repository

git clone https://github.com/your-username/career-predictor.git


Navigate to project folder

cd career_predictor2


Install dependencies

pip install -r requirements.txt


Run the application

python app.py


Open in browser

http://127.0.0.1:5000

🧠 Machine Learning Model

The ML model is trained separately and saved as model.pkl

Encoders are used to convert categorical input into numerical form

The predicted career is mapped back using inverse encoding

🔒 Authentication Logic

Users can login or signup using Email or Phone

Duplicate signup is restricted

Session-based authentication ensures secure access

📌 Future Improvements

✅ Password authentication

✅ User profile & settings page

✅ Admin dashboard

✅ Deployment on Render / Railway / Heroku

✅ Mobile responsive UI

👩‍💻 Author

Poorvi Saini
🎓 Student | 💻 Web Developer | 🤖 ML Enthusiast

⭐ Acknowledgement

This project was created for learning, practice, and academic purposes, combining Flask, Machine Learning, and Database concepts into one real-world-project
