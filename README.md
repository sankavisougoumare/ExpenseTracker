# 💰 Expense Tracker - Data Analytics & Web Application

## 📌 Project Overview

The Expense Tracker is a data analytics web application built with Python, Flask, SQLite, Pandas, NumPy, Matplotlib, and Chart.js.

It provides a interactive web interface for tracking personal expenses, analyzing spending patterns, detecting budget overspending, running custom SQL queries, and exporting data reports.

---

## 🚀 How to Run the Web Application

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Web Server**
   ```bash
   python3 app.py
   ```

3. **Open in Browser**
   Navigate to: [http://127.0.0.1:5001](http://127.0.0.1:5001)

---

## 🌐 Web Application Features

- **📊 Analytics Dashboard**: Live KPI metric cards (Total Expense, Average Expense, Highest & Lowest Transactions) and interactive Chart.js graphs (Category Breakdown, Payment Methods, Daily & Monthly Trends).
- **💳 Expense CRUD Management**: Search, filter by category, add new expenses, edit existing records, and delete expenses with real-time SQLite sync.
- **🎯 Budget & Alert Monitor**: Track budget progress per category (Food, Transport, Shopping, Entertainment, etc.), view remaining limits, and receive automatic **WARNING** and **OVER BUDGET** alerts.
- **💻 Live SQL Console**: Run custom `SELECT` SQL queries directly in the browser with instant tabular results.
- **📁 CSV Data Import / Export**: Upload new expense CSV datasets or export the current SQLite database to CSV format.

---

## 🛠 Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Chart.js, FontAwesome
- **Backend**: Python 3, Flask REST API
- **Database**: SQLite3
- **Data Analytics**: Pandas, NumPy, Matplotlib

---

## 📂 Project Structure

```text
expense/
│
├── app.py                     # Flask web application server & REST APIs
├── requirements.txt           # Python package dependencies
├── templates/
│   └── index.html             # Responsive Web Dashboard Interface
│
├── data/
│   └── data.csv               # Initial sample dataset
│
├── outputs/
│   └── expense.db             # SQLite database storing expenses & budgets
│
├── src/                       # Analytical scripts
│   ├── expense_analysis.py
│   ├── database.py
│   ├── dashboard.py
│   └── budget_analysis.py
│
└── README.md
```