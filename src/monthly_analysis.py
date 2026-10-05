import pandas as pd
import matplotlib.pyplot as plt
import os

# ==============================
# PATHS
# ==============================

DATA_PATH = "outputs/clean_expense_data.csv"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================
# LOAD CLEAN DATA
# ==============================

df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])


# ==============================
# MONTHLY EXPENSE
# ==============================

monthly_expense = (
    df.groupby(["year", "month", "month_name"])["amount"]
    .sum()
    .reset_index()
)

monthly_expense = monthly_expense.sort_values(
    ["year", "month"]
)

print("\n================================")
print("       MONTHLY EXPENSE")
print("================================")

print(monthly_expense)


# ==============================
# HIGHEST SPENDING MONTH
# ==============================

highest_month = monthly_expense.loc[
    monthly_expense["amount"].idxmax()
]

print("\n================================")
print("       HIGHEST SPENDING MONTH")
print("================================")

print(
    highest_month["month_name"],
    "-",
    highest_month["amount"]
)


# ==============================
# DAILY EXPENSE
# ==============================

daily_expense = (
    df.groupby("date")["amount"]
    .sum()
    .reset_index()
)

print("\n================================")
print("       DAILY EXPENSE")
print("================================")

print(daily_expense)


# ==============================
# HIGHEST SPENDING DAY
# ==============================

highest_day = daily_expense.loc[
    daily_expense["amount"].idxmax()
]

print("\n================================")
print("       HIGHEST SPENDING DAY")
print("================================")

print(
    highest_day["date"].date(),
    "-",
    highest_day["amount"]
)


# ==============================
# CATEGORY BY MONTH
# ==============================

category_month = pd.pivot_table(
    df,
    values="amount",
    index="month_name",
    columns="category",
    aggfunc="sum",
    fill_value=0
)

print("\n================================")
print("       CATEGORY BY MONTH")
print("================================")

print(category_month)


# ==============================
# SAVE RESULTS
# ==============================

monthly_expense.to_csv(
    f"{OUTPUT_DIR}/monthly_expense.csv",
    index=False
)

daily_expense.to_csv(
    f"{OUTPUT_DIR}/daily_expense.csv",
    index=False
)

category_month.to_csv(
    f"{OUTPUT_DIR}/category_month_analysis.csv"
)


# ==============================
# MONTHLY CHART
# ==============================

plt.figure(figsize=(8, 5))

plt.plot(
    monthly_expense["month_name"],
    monthly_expense["amount"],
    marker="o"
)

plt.title("Monthly Expense Trend")
plt.xlabel("Month")
plt.ylabel("Total Expense")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/monthly_expense.png"
)

plt.show()


# ==============================
# CATEGORY CHART
# ==============================

category_totals = (
    df.groupby("category")["amount"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 5))

category_totals.plot(kind="bar")

plt.title("Expense by Category")
plt.xlabel("Category")
plt.ylabel("Total Expense")

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/category_expense.png"
)

plt.show()


print("\n================================")
print("Monthly analysis completed!")
print("Results saved in outputs folder.")
print("================================")