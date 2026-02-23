# Smart Campus Management System

The Smart Campus Management System is a comprehensive Django-based web application designed to streamline and automate various campus operations. This project integrates multiple modules ranging from attendance tracking to food stall pre-ordering and AI-based analytics.

## Features and Modules

The system is composed of several independent but integrated Django apps:

### 1. 🎓 Core Campus Management (`core` & `_core_hub`)
- Centralized hub for managing students, faculty, and courses.
- User management and authentication system (custom user model `food_stall.User`).
- Dashboard for quick access to various campus services.

### 2. 🍔 Smart Food Stall Pre-Ordering System (`food_stall`)
- Allows students and staff to browse menus from various campus food stalls (e.g., Nand Juice, NK, Amritzari Zaika, Chai Sutta Bar, etc.).
- Pre-order meals to avoid long queues during breaks.
- Order tracking and management for food stall vendors.

### 3. 📅 Attendance Tracking Module (`attendance`)
- Subject-based attendance tracking tailored for individual courses.
- Daily attendance marking and monitoring.
- Interactive dashboard for viewing attendance statistics.

### 4. 📚 Make-Up Class & Remedial Module (`remedial`)
- Empowers faculty to schedule make-up classes and remedial sessions.
- Generates specific remedial codes for students to mark attendance.
- Simplifies the process of catching up on missed lectures and tracking participation.

### 5. 🤖 AI Engine (`ai_engine`)
- Integrates machine learning for campus analytics.
- Uses tools like `pandas` and `scikit-learn` for data processing and predictive analytics (such as predicting attendance trends or student performance).

## Technology Stack

- **Backend:** Python 3, Django 5.x
- **Frontend:** HTML5, CSS3, JavaScript, Django Templates
- **Database:** SQLite (Default for development)
- **Machine Learning / AI:** Scikit-learn, Pandas
- **Data Validation:** JSONSchema

## Prerequisites

Before running the project locally, ensure you have the following installed:
- Python 3.10+
- pip (Python package installer)

## Installation and Setup

Follow these steps to set up the project locally:

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd "Pep Project"
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Directory Structure
```text
Pep Project/
│
├── ai_engine/          # AI predictive analytics module
├── attendance/         # Attendance tracking application
├── core/               # Core utility and management application
├── _core_hub/          # Central hub configuration
├── food_stall/         # Food ordering module and custom User model
├── remedial/           # Make-up class and remedial code module
├── smart_campus/       # Main Django project settings and URLs
├── static/             # Static files (CSS, JS, Images)
├── templates/          # Global HTML templates
│
├── manage.py           # Django command-line utility
├── requirements.txt    # Project Python dependencies
└── db.sqlite3          # SQLite database
```

## Contributing
Contributions are welcome! Please create a feature branch and submit a pull request with your changes. Ensure that your code adheres to standard Django practices.
