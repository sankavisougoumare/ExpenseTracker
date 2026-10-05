import os
import sys
import site

# Ensure user site-packages directory is in sys.path
user_site = site.getusersitepackages()
if user_site and user_site not in sys.path:
    sys.path.insert(0, user_site)

import sqlite3
import pandas as pd
import numpy as np
import io
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server rendering
import matplotlib.pyplot as plt

from flask import Flask, render_template, request, jsonify, send_file, Response

app = Flask(__name__, static_folder='static', template_folder='templates')

DB_DIR = os.path.join(os.path.dirname(__file__), 'outputs')
DB_PATH = os.path.join(DB_DIR, 'expense.db')
DATA_CSV = os.path.join(os.path.dirname(__file__), 'data', 'data.csv')

DEFAULT_BUDGETS = {
    "Food": 1000.0,
    "Transport": 500.0,
    "Shopping": 2000.0,
    "Entertainment": 1000.0,
    "Bills": 2000.0,
    "Health": 1000.0
}

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create expenses table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    # Create budgets table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            category TEXT PRIMARY KEY,
            budget_limit REAL NOT NULL
        )
    ''')
    
    # Insert default budgets if empty
    cursor.execute("SELECT COUNT(*) FROM budgets")
    if cursor.fetchone()[0] == 0:
        for cat, limit in DEFAULT_BUDGETS.items():
            cursor.execute("INSERT OR REPLACE INTO budgets (category, budget_limit) VALUES (?, ?)", (cat, limit))
            
    # Check if expenses table is empty; if so, populate from data.csv if available
    cursor.execute("SELECT COUNT(*) FROM expenses")
    if cursor.fetchone()[0] == 0 and os.path.exists(DATA_CSV):
        try:
            df = pd.read_csv(DATA_CSV)
            for _, row in df.iterrows():
                cursor.execute('''
                    INSERT INTO expenses (date, category, amount, payment_method, description)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    str(row.get('date', '')),
                    str(row.get('category', '')),
                    float(row.get('amount', 0)),
                    str(row.get('payment_method', '')),
                    str(row.get('description', ''))
                ))
        except Exception as e:
            print("Error auto-populating database from CSV:", e)
            
    conn.commit()
    conn.close()

# Initialize DB on server start
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/summary', methods=['GET'])
def get_summary():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    
    if df.empty:
        return jsonify({
            'total_expense': 0,
            'average_expense': 0,
            'transaction_count': 0,
            'highest_expense': None,
            'lowest_expense': None,
            'category_summary': [],
            'payment_summary': [],
            'monthly_summary': [],
            'daily_summary': []
        })
    
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
    total_expense = float(df['amount'].sum())
    average_expense = float(df['amount'].mean())
    transaction_count = int(len(df))
    
    highest_idx = df['amount'].idxmax()
    highest_row = df.loc[highest_idx].to_dict() if not df.empty else None
    
    lowest_idx = df['amount'].idxmin()
    lowest_row = df.loc[lowest_idx].to_dict() if not df.empty else None

    # Category breakdown
    cat_df = df.groupby('category')['amount'].agg(['sum', 'count']).reset_index()
    cat_df['percentage'] = (cat_df['sum'] / total_expense * 100) if total_expense > 0 else 0
    cat_df = cat_df.sort_values(by='sum', ascending=False)
    category_summary = [
        {
            'category': row['category'],
            'total': float(row['sum']),
            'count': int(row['count']),
            'percentage': round(float(row['percentage']), 1)
        }
        for _, row in cat_df.iterrows()
    ]

    # Payment method breakdown
    pay_df = df.groupby('payment_method')['amount'].agg(['sum', 'count']).reset_index()
    pay_df = pay_df.sort_values(by='sum', ascending=False)
    payment_summary = [
        {
            'payment_method': row['payment_method'],
            'total': float(row['sum']),
            'count': int(row['count'])
        }
        for _, row in pay_df.iterrows()
    ]

    # Monthly breakdown (format YYYY-MM)
    df['month'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m')
    month_df = df.groupby('month')['amount'].sum().reset_index().sort_values(by='month')
    monthly_summary = [
        {'month': str(row['month']), 'total': float(row['amount'])}
        for _, row in month_df.iterrows() if pd.notnull(row['month'])
    ]

    # Daily breakdown
    daily_df = df.groupby('date')['amount'].sum().reset_index().sort_values(by='date')
    daily_summary = [
        {'date': str(row['date']), 'total': float(row['amount'])}
        for _, row in daily_df.iterrows()
    ]

    return jsonify({
        'total_expense': round(total_expense, 2),
        'average_expense': round(average_expense, 2),
        'transaction_count': transaction_count,
        'highest_expense': highest_row,
        'lowest_expense': lowest_row,
        'category_summary': category_summary,
        'payment_summary': payment_summary,
        'monthly_summary': monthly_summary,
        'daily_summary': daily_summary
    })

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    category = request.args.get('category')
    search = request.args.get('search')
    sort_by = request.args.get('sort_by', 'date')
    order = request.args.get('order', 'DESC')
    
    valid_sorts = ['date', 'amount', 'category', 'payment_method', 'id']
    if sort_by not in valid_sorts:
        sort_by = 'date'
        
    order_clause = 'DESC' if order.upper() == 'DESC' else 'ASC'

    query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if search:
        query += " AND (description LIKE ? OR category LIKE ? OR payment_method LIKE ?)"
        wildcard = f"%{search}%"
        params.extend([wildcard, wildcard, wildcard])

    query += f" ORDER BY {sort_by} {order_clause}"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    expenses = [dict(row) for row in rows]
    return jsonify(expenses)

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.get_json() or {}
    date = data.get('date')
    category = data.get('category')
    amount = data.get('amount')
    payment_method = data.get('payment_method')
    description = data.get('description', '')

    if not date or not category or amount is None or not payment_method:
        return jsonify({'error': 'Missing required fields: date, category, amount, payment_method'}), 400

    try:
        amount_val = float(amount)
    except ValueError:
        return jsonify({'error': 'Amount must be a valid number'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (date, category, amount, payment_method, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, category, amount_val, payment_method, description))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({'message': 'Expense added successfully', 'id': new_id}), 201

@app.route('/api/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    data = request.get_json() or {}
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Expense not found'}), 404

    date = data.get('date')
    category = data.get('category')
    amount = data.get('amount')
    payment_method = data.get('payment_method')
    description = data.get('description')

    cursor.execute('''
        UPDATE expenses
        SET date = COALESCE(?, date),
            category = COALESCE(?, category),
            amount = COALESCE(?, amount),
            payment_method = COALESCE(?, payment_method),
            description = COALESCE(?, description)
        WHERE id = ?
    ''', (date, category, amount, payment_method, description, expense_id))
    
    conn.commit()
    conn.close()
    return jsonify({'message': 'Expense updated successfully'})

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()

    if deleted == 0:
        return jsonify({'error': 'Expense not found'}), 404

    return jsonify({'message': 'Expense deleted successfully'})

@app.route('/api/budgets', methods=['GET'])
def get_budgets():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT category, budget_limit FROM budgets")
    budget_map = {row['category']: row['budget_limit'] for row in cursor.fetchall()}

    df = pd.read_sql_query("SELECT category, SUM(amount) as spent FROM expenses GROUP BY category", conn)
    conn.close()

    spent_map = {}
    if not df.empty:
        spent_map = dict(zip(df['category'], df['spent']))

    all_categories = set(budget_map.keys()).union(set(spent_map.keys()))

    results = []
    for cat in sorted(all_categories):
        limit = budget_map.get(cat, DEFAULT_BUDGETS.get(cat, 1500.0))
        spent = float(spent_map.get(cat, 0.0))
        remaining = limit - spent

        if spent > limit:
            status = "OVER BUDGET"
        elif spent >= limit * 0.8:
            status = "WARNING"
        else:
            status = "WITHIN BUDGET"

        results.append({
            'category': cat,
            'budget': limit,
            'spent': spent,
            'remaining': remaining,
            'status': status,
            'percentage_used': round((spent / limit * 100), 1) if limit > 0 else 0
        })

    return jsonify(results)

@app.route('/api/budgets', methods=['POST'])
def set_budget():
    data = request.get_json() or {}
    category = data.get('category')
    budget_limit = data.get('budget_limit')

    if not category or budget_limit is None:
        return jsonify({'error': 'Category and budget_limit are required'}), 400

    try:
        limit_val = float(budget_limit)
    except ValueError:
        return jsonify({'error': 'budget_limit must be a number'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO budgets (category, budget_limit) VALUES (?, ?)", (category, limit_val))
    conn.commit()
    conn.close()

    return jsonify({'message': f'Budget for {category} updated to {limit_val}'})

@app.route('/api/import-csv', methods=['POST'])
def import_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        df = pd.read_csv(file)
        required_cols = {'date', 'category', 'amount', 'payment_method'}
        if not required_cols.issubset(set(df.columns)):
            return jsonify({'error': f'CSV missing required columns: {required_cols - set(df.columns)}'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Option to clear existing or append (we append)
        replace_mode = request.form.get('replace', 'false').lower() == 'true'
        if replace_mode:
            cursor.execute("DELETE FROM expenses")

        imported_count = 0
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO expenses (date, category, amount, payment_method, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                str(row['date']),
                str(row['category']),
                float(row['amount']),
                str(row['payment_method']),
                str(row.get('description', ''))
            ))
            imported_count += 1

        conn.commit()
        conn.close()

        return jsonify({'message': f'Successfully imported {imported_count} records'})
    except Exception as e:
        return jsonify({'error': f'Failed to process CSV file: {str(e)}'}), 500

@app.route('/api/export-csv', methods=['GET'])
def export_csv():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT date, category, amount, payment_method, description FROM expenses ORDER BY date DESC", conn)
    conn.close()

    csv_data = df.to_csv(index=False)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=expenses_export.csv"}
    )

@app.route('/api/sql', methods=['POST'])
def run_sql():
    data = request.get_json() or {}
    query = data.get('query', '').strip()

    if not query:
        return jsonify({'error': 'SQL query is empty'}), 400

    # Basic safety check: allow SELECT queries
    if not query.upper().startswith('SELECT'):
        return jsonify({'error': 'Only SELECT SQL queries are allowed in this web console.'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [description[0] for description in cursor.description] if cursor.description else []
        rows = [list(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify({
            'columns': columns,
            'rows': rows,
            'row_count': len(rows)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/charts/category.png', methods=['GET'])
def chart_category_png():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT category, SUM(amount) as total FROM expenses GROUP BY category ORDER BY total DESC", conn)
    conn.close()

    plt.figure(figsize=(7, 4.5))
    if not df.empty:
        plt.bar(df['category'], df['total'], color='#4F46E5', edgecolor='#3730A3', linewidth=1)
        plt.title('Total Expenses by Category', fontsize=12, fontweight='bold', pad=12)
        plt.xlabel('Category', fontsize=10)
        plt.ylabel('Amount (₹)', fontsize=10)
        plt.xticks(rotation=25)
        plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120)
    buf.seek(0)
    plt.close()

    return send_file(buf, mimetype='image/png')

@app.route('/api/charts/monthly.png', methods=['GET'])
def chart_monthly_png():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT date, amount FROM expenses", conn)
    conn.close()

    plt.figure(figsize=(7, 4.5))
    if not df.empty:
        df['month'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m')
        m_df = df.groupby('month')['amount'].sum().reset_index().sort_values(by='month')
        plt.plot(m_df['month'], m_df['amount'], marker='o', color='#10B981', linewidth=2, markersize=6)
        plt.title('Monthly Expense Trend', fontsize=12, fontweight='bold', pad=12)
        plt.xlabel('Month', fontsize=10)
        plt.ylabel('Amount (₹)', fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120)
    buf.seek(0)
    plt.close()

    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    print("Starting Expense Tracker Web App on http://127.0.0.1:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
