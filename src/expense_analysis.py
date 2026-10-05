import pandas as pd
import matplotlib.pyplot as plt
import os

# ==============================
# 1. LOAD DATA
# ==============================

DATA_PATH = "data/data.csv"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

print("\n================================")
print("       EXPENSE TRACKER")
print("================================")

print("\nFirst 5 Records:")
print(df.head())


# ==============================
# 2. DATA INFORMATION
# ==============================

print("\n================================")
print("       DATA INFORMATION")
print("================================")

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nColumn Names:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())


# ==============================
# 3. TOTAL EXPENSE
# ==============================

total_expense = df["amount"].sum()

average_expense = df["amount"].mean()
maximum_expense = df["amount"].max()
minimum_expense = df["amount"].min()

print("\n================================")
print("       EXPENSE SUMMARY")
print("================================")

print("Total Expense:", total_expense)
print("Average Expense:", round(average_expense, 2))
print("Maximum Expense:", maximum_expense)
print("Minimum Expense:", minimum_expense)


# ==============================
# 4. CATEGORY ANALYSIS
# ==============================

category_expense = (
    df.groupby("category")["amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\n================================")
print("       CATEGORY ANALYSIS")
print("================================")

print(category_expense)

category_expense.to_csv(
    f"{OUTPUT_DIR}/category_expense.csv"
)


# ==============================
# 5. PAYMENT METHOD ANALYSIS
# ==============================

payment_analysis = (
    df.groupby("payment_method")["amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\n================================")
print("       PAYMENT ANALYSIS")
print("================================")

print(payment_analysis)

payment_analysis.to_csv(
    f"{OUTPUT_DIR}/payment_analysis.csv"
)


# ==============================
# 6. HIGHEST EXPENSE
# ==============================

highest_expense = df.loc[df["amount"].idxmax()]

print("\n================================")
print("       HIGHEST EXPENSE")
print("================================")

print(highest_expense)


# ==============================
# 7. CATEGORY CHART
# ==============================

plt.figure(figsize=(8, 5))

category_expense.plot(kind="bar")

plt.title("Total Expense by Category")
plt.xlabel("Category")
plt.ylabel("Amount")

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/expense_by_category.png"
)

plt.show()


# ==============================
# 8. SUMMARY FILE
# ==============================

summary = pd.DataFrame({
    "metric": [
        "Total Expense",
        "Average Expense",
        "Maximum Expense",
        "Minimum Expense"
    ],
    "value": [
        total_expense,
        average_expense,
        maximum_expense,
        minimum_expense
    ]
})

summary.to_csv(
    f"{OUTPUT_DIR}/expense_summary.csv",
    index=False
)


# ==============================
# COMPLETED
# ==============================

print("\n================================")
print("Analysis completed successfully!")
print("Results saved in outputs folder.")
print("================================")