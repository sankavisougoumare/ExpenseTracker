import pandas as pd
import os

# ==============================
# PATHS
# ==============================

DATA_PATH = "data/data.csv"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================
# LOAD DATA
# ==============================

df = pd.read_csv(DATA_PATH)

print("\n================================")
print("       DATA CLEANING")
print("================================")

print("\nOriginal Data:")
print(df)


# ==============================
# REMOVE DUPLICATES
# ==============================

duplicates = df.duplicated().sum()

print("\nDuplicate Rows:", duplicates)

df = df.drop_duplicates()


# ==============================
# HANDLE MISSING VALUES
# ==============================

print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

# Remove rows with missing important values
df = df.dropna(
    subset=["date", "category", "amount"]
)


# ==============================
# CLEAN TEXT COLUMNS
# ==============================

df["category"] = df["category"].str.strip().str.title()

df["payment_method"] = (
    df["payment_method"]
    .str.strip()
    .str.upper()
)

df["description"] = (
    df["description"]
    .str.strip()
)


# ==============================
# CONVERT DATE
# ==============================

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)


# ==============================
# CONVERT AMOUNT
# ==============================

df["amount"] = pd.to_numeric(
    df["amount"],
    errors="coerce"
)


# ==============================
# REMOVE INVALID VALUES
# ==============================

df = df.dropna(
    subset=["date", "amount"]
)

df = df[df["amount"] >= 0]


# ==============================
# SORT DATA
# ==============================

df = df.sort_values("date")


# ==============================
# CREATE NEW FEATURES
# ==============================

df["month"] = df["date"].dt.month

df["month_name"] = df["date"].dt.strftime("%B")

df["year"] = df["date"].dt.year

df["day"] = df["date"].dt.day_name()


# ==============================
# SAVE CLEAN DATA
# ==============================

output_path = "outputs/clean_expense_data.csv"

df.to_csv(
    output_path,
    index=False
)


# ==============================
# FINAL INFORMATION
# ==============================

print("\n================================")
print("       CLEAN DATA")
print("================================")

print(df)

print("\nRows after cleaning:", len(df))

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

print("\nClean dataset saved to:")
print(output_path)

print("\n================================")
print("Data cleaning completed!")
print("================================")