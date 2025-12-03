# 🔮 AI Salary Predictor (Pure ML)

A Full-Stack Machine Learning Web Application that predicts salaries based on **Experience** and **Skill Level**.

Unlike simple rule-based systems, this project uses **Linear Regression (Scikit-Learn)** to learn mathematical patterns directly from a database. It features a Cyberpunk/Glassmorphism UI and a real-time Training Dashboard where you can teach the AI new patterns.

## 🛡️ Badges
![Status](https://img.shields.io/badge/Status-Completed-success)
[![GitHub repository](https://img.shields.io/badge/GitHub-arka--001%2FSalary--Predictor-blue?logo=github)](https://github.com/arka-001/Salary-Predictor)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-DRF-green)
![ML](https://img.shields.io/badge/Scikit--Learn-orange)

---

## 🚀 Features

*   **Pure Machine Learning:** No hardcoded `if/else` rules. The AI dynamically calculates salaries using Multi-Variable Linear Regression: $Salary = m_1(Years) + m_2(Level) + c$.
*   **Dual-Interface:**
    *   **User Panel:** Predicts salaries with a Yearly/Monthly breakdown and interactive Market Trend Graph (Chart.js).
    *   **Admin Dashboard:** Allows adding, deleting, and resetting training data.
*   **Real-Time Learning:** The model retrains instantly whenever data is modified in the dashboard.
*   **Persistent Storage:** Uses SQLite to store dataset permanently.
*   **Modern UI:** Glassmorphism design, gradient animations, and responsive layout.

---

## 🛠️ Tech Stack

*   **Backend:** Python, Django, Django REST Framework (DRF)
*   **Machine Learning:** Scikit-Learn, Pandas, NumPy
*   **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
*   **Visualization**: Chart.js
*   **Database:** SQLite

---

## 📂 Project Structure

The project follows a standard Django structure, separating the core configuration from the main predictor application.

```
Salary Predictor/
│
├── core/                   # Django Project Configuration
│   ├── settings.py
│   └── urls.py             # URL Routing
│
├── predictor/              # Main Application
│   ├── models.py           # Database Schema (SalaryData)
│   ├── views.py            # AI Logic & API Views
│   ├── templates/          # HTML Files
│   │   ├── index.html      # Prediction UI
│   │   └── train.html      # Admin Dashboard UI
│   └── ...
│
├── db.sqlite3              # SQLite Database
├── manage.py               # Django Command Utility
└── requirements.txt        # Library Dependencies
```

---

## 👨‍💻 Logic Behind the AI

This project uses **Multiple Linear Regression**.

The AI tries to find the best-fit plane equation:

`Salary = (m1 × Years) + (m2 × Level) + Intercept`

Where:
*   **m1**: The value of 1 extra year of experience.
*   **m2**: The value of 1 extra skill level.

When you add data in the dashboard, Scikit-Learn recalculates **m1** and **m2** instantly to minimize the error (Mean Squared Error).

---

## 📦 Installation Guide

Follow these steps to run the project locally.

### 1. Prerequisite
Make sure you have Python installed.

### 2. Create Virtual Environment
Open your terminal in the project folder:
```bash
# Create Environment
python -m venv venv

# Activate (Windows):
.\venv\Scripts\activate

# Activate (Mac/Linux):
source venv/bin/activate
```

### 3. Set up a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

Install all the required packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations

This will create the necessary database tables (for `SalaryData`).

```bash
python manage.py migrate
```

### 6. Run the Development Server

Start the Django development server.

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

---

## 📖 How to Use

### Predictor Page (`/`)

1.  Navigate to the home page.
2.  Enter the **Years of Experience**.
3.  Use the slider to set the **Skill Level** (from 1 to 10).
4.  Click the **PREDICT SALARY** button.
5.  The predicted yearly and monthly salary will appear, and a point will be plotted on the graph.

### Training Dashboard (`/train/`)

1.  Click the "⚙️ Open Training Dashboard" link from the home page.
2.  **Add Data**: Fill in the "Years Experience", "Skill Level", and "Salary" fields and click **+ Add Data**. The page will reload, and the AI will be retrained.
3.  **Delete Data**: Click the `✕` button on any row to delete that data point. The AI will be retrained.
4.  **Reset Data**: Click the **🔄 Reset to Default Data** button to clear the entire database and load a predefined set of default entries.
5.  **Delete All Data**: Click the **🗑️ Delete All Data** button to permanently remove all training data from the database. The AI will be retrained.

---

## 📝 API Documentation

The application exposes several REST API endpoints for programmatic access.

**Base URL**: `http://127.0.0.1:8000/api/`

### 1. Predict Salary

*   **Endpoint**: `POST /api/predict/`
*   **Description**: Predicts a salary based on input features.
*   **Request Body**:
    ```json
    {
        "years": 5.5,
        "level": 8
    }
    ```
*   **Success Response (200 OK)**:
    ```json
    {
        "yearly": "₹ 2,500,000",
        "monthly": "₹ 208,333",
        "raw": 2500000.0
    }
    ```

### 2. Add Training Data

*   **Endpoint**: `POST /api/train/`
*   **Description**: Adds a new data point to the database and retrains the model.
*   **Request Body**:
    ```json
    {
        "years": 12,
        "level": 9,
        "salary": 6000000
    }
    ```
*   **Success Response (200 OK)**: `{"message": "Success"}`

### 3. Delete a Data Point

*   **Endpoint**: `POST /api/delete/`
*   **Description**: Deletes a data point by its ID and retrains the model.
*   **Request Body**: `{"id": 1}`
*   **Success Response (200 OK)**: `{"message": "Deleted"}`

### 4. Reset to Defaults

*   **Endpoint**: `POST /api/reset/`
*   **Description**: Deletes all existing data and loads a predefined default dataset.
*   **Request Body**: (None)
*   **Success Response (200 OK)**: `{"message": "Defaults Loaded"}`

### 5. Delete All Data

*   **Endpoint**: `POST /api/delete-all/`
*   **Description**: Deletes all data points from the database and retrains the model.
*   **Request Body**: (None)
*   **Success Response (200 OK)**:
    ```json
    {
        "message": "Deleted all 7 data points",
        "count": 7
    }
    ```

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

### 6. Get Training Stats
*   **Endpoint**: `GET /api/training-stats/`
*   **Description**: Retrieves statistics about the current training data.
*   **Request Body**: (None)
*   **Success Response (200 OK)**:
    ```json
    {
        "data_points": 7,
        "average_salary": 2042857.14,
        "avg_experience": 4.85
    }
    ```