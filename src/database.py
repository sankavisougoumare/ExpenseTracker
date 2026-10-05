import sqlite3
import pandas as pd
import os

# ==========================================
# PATHS
# ==========================================

DATA_PATH = "outputs/clean_expense_data.csv"
DATABASE_PATH = "outputs/expense.db"

# ==========================================
# LOAD CLEAN DATA
# ==========================================

df = pd.read_csv(DATA_PATH)

print("\n================================")
print("       EXPENSE DATABASE")
print("================================")

print("Loading:", len(df), "records")


# ==========================================
# CREATE SQLITE DATABASE
# ==========================================

connection = sqlite3.connect(DATABASE_PATH)

df.to_sql(
    "expenses",
    connection,
    if_exists="replace",
    index=False
)

print("\nDatabase created successfully!")
print("Database:", DATABASE_PATH)


# ==========================================
# FUNCTION TO RUN SQL
# ==========================================

def run_query(query, title):

    print("\n================================")
    print(title)
    print("================================")

    result = pd.read_sql_query(
        query,
        connection
    )

    print(result)

    return result


# ==========================================
# 1. TOTAL EXPENSE
# ==========================================

run_query(
    """
    SELECT SUM(amount) AS total_expense
    FROM expenses
    """,
    "TOTAL EXPENSE"
)


# ==========================================
# 2. AVERAGE EXPENSE
# ==========================================

run_query(
    """
    SELECT ROUND(AVG(amount), 2) AS average_expense
    FROM expenses
    """,
    "AVERAGE EXPENSE"
)


# ==========================================
# 3. CATEGORY ANALYSIS
# ==========================================

run_query(
    """
    SELECT
        category,
        SUM(amount) AS total_expense
    FROM expenses
    GROUP BY category
    ORDER BY total_expense DESC
    """,
    "EXPENSE BY CATEGORY"
)


# ==========================================
# 4. PAYMENT METHOD
# ==========================================

run_query(
    """
    SELECT
        payment_method,
        SUM(amount) AS total_expense
    FROM expenses
    GROUP BY payment_method
    ORDER BY total_expense DESC
    """,
    "EXPENSE BY PAYMENT METHOD"
)


# ==========================================
# 5. HIGHEST EXPENSE
# ==========================================

run_query(
    """
    SELECT *
    FROM expenses
    ORDER BY amount DESC
    LIMIT 1
    """,
    "HIGHEST EXPENSE"
)


# ==========================================
# 6. DAILY EXPENSE
# ==========================================

run_query(
    """
    SELECT
        date,
        SUM(amount) AS daily_expense
    FROM expenses
    GROUP BY date
    ORDER BY date
    """,
    "DAILY EXPENSE"
)


# ==========================================
# 7. TRANSACTION COUNT
# ==========================================

run_query(
    """
    SELECT
        category,
        COUNT(*) AS transaction_count
    FROM expenses
    GROUP BY category
    ORDER BY transaction_count DESC
    """,
    "TRANSACTIONS BY CATEGORY"
)


# ==========================================
# CLOSE DATABASE
# ==========================================

connection.close()

print("\n================================")
print("SQL ANALYSIS COMPLETED!")
print("================================")