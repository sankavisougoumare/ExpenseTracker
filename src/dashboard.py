import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# DATABASE CONNECTION
# ==========================================

connection = sqlite3.connect("outputs/expense.db")

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_sql_query(
    "SELECT * FROM expenses",
    connection
)

# ==========================================
# KPI CALCULATIONS
# ==========================================

total_expense = df["amount"].sum()
average_expense = df["amount"].mean()
transaction_count = len(df)

highest_expense = df["amount"].max()

# ==========================================
# DISPLAY DASHBOARD
# ==========================================

print("\n")
print("==============================================")
print("             EXPENSE TRACKER")
print("             ANALYTICS DASHBOARD")
print("==============================================")

print(f"\nTotal Expense       : ₹{total_expense:,.2f}")
print(f"Average Expense     : ₹{average_expense:,.2f}")
print(f"Transactions        : {transaction_count}")
print(f"Highest Expense     : ₹{highest_expense:,.2f}")


# ==========================================
# CATEGORY ANALYSIS
# ==========================================

category_data = pd.read_sql_query(
    """
    SELECT
        category,
        SUM(amount) AS total
    FROM expenses
    GROUP BY category
    ORDER BY total DESC
    """,
    connection
)

print("\n==============================================")
print("             CATEGORY ANALYSIS")
print("==============================================")

print(category_data)


# ==========================================
# PAYMENT ANALYSIS
# ==========================================

payment_data = pd.read_sql_query(
    """
    SELECT
        payment_method,
        SUM(amount) AS total
    FROM expenses
    GROUP BY payment_method
    ORDER BY total DESC
    """,
    connection
)

print("\n==============================================")
print("             PAYMENT ANALYSIS")
print("==============================================")

print(payment_data)


# ==========================================
# CREATE DASHBOARD CHARTS
# ==========================================

plt.figure(figsize=(8, 5))

plt.bar(
    category_data["category"],
    category_data["total"]
)

plt.title("Expense by Category")
plt.xlabel("Category")
plt.ylabel("Total Expense")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "outputs/dashboard_category.png"
)

plt.show()


# ==========================================
# PAYMENT METHOD CHART
# ==========================================

plt.figure(figsize=(8, 5))

plt.bar(
    payment_data["payment_method"],
    payment_data["total"]
)

plt.title("Expense by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Total Expense")

plt.tight_layout()

plt.savefig(
    "outputs/dashboard_payment.png"
)

plt.show()


# ==========================================
# CLOSE DATABASE
# ==========================================

connection.close()

print("\n==============================================")
print("Dashboard analysis completed successfully!")
print("Charts saved in outputs folder.")
print("==============================================")