import sqlite3
import pandas as pd

# ==========================================
# DATABASE
# ==========================================

connection = sqlite3.connect("outputs/expense.db")

df = pd.read_sql_query(
    "SELECT * FROM expenses",
    connection
)

# ==========================================
# BUDGET LIMITS
# ==========================================

budgets = {
    "Food": 1000,
    "Transport": 500,
    "Shopping": 2000,
    "Entertainment": 1000,
    "Bills": 2000,
    "Health": 1000
}

# ==========================================
# CATEGORY SPENDING
# ==========================================

category_expense = (
    df.groupby("category")["amount"]
    .sum()
)

print("\n==============================================")
print("        BUDGET & OVERSPENDING ANALYSIS")
print("==============================================")

results = []

for category, spent in category_expense.items():

    budget = budgets.get(category, 1500)

    remaining = budget - spent

    if spent > budget:
        status = "OVER BUDGET"
    elif spent >= budget * 0.8:
        status = "WARNING"
    else:
        status = "WITHIN BUDGET"

    results.append({
        "category": category,
        "budget": budget,
        "spent": spent,
        "remaining": remaining,
        "status": status
    })


# ==========================================
# RESULT
# ==========================================

budget_df = pd.DataFrame(results)

print(budget_df.to_string(index=False))


# ==========================================
# SAVE REPORT
# ==========================================

budget_df.to_csv(
    "outputs/budget_report.csv",
    index=False
)


# ==========================================
# OVERSPENDING ALERTS
# ==========================================

print("\n==============================================")
print("             ALERTS")
print("==============================================")

alerts = budget_df[
    budget_df["status"] == "OVER BUDGET"
]

if len(alerts) == 0:

    print("No categories are over budget.")

else:

    for _, row in alerts.iterrows():

        print(
            f"⚠ {row['category']} is over budget "
            f"by ₹{row['spent'] - row['budget']:.2f}"
        )


# ==========================================
# CLOSE
# ==========================================

connection.close()

print("\n==============================================")
print("Budget analysis completed!")
print("Report saved: outputs/budget_report.csv")
print("==============================================")