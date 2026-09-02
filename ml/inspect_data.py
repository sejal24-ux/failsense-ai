import pandas as pd

# Load dataset
df = pd.read_csv("data/transactions.csv")

print("=" * 60)
print("FAILSENSE AI - DATASET INSPECTION")
print("=" * 60)

# 1. Dataset size
print("\n1. DATASET SIZE")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# 2. Column names
print("\n2. COLUMNS")
print(df.columns.tolist())

# 3. First 5 transactions
print("\n3. FIRST 5 TRANSACTIONS")
print(df.head())

# 4. Transaction status
print("\n4. TRANSACTION STATUS")
print(df["status"].value_counts())

# 5. Failure percentage
failure_rate = (
    df["status"].eq("FAILED").mean() * 100
)

print(
    f"\nOverall Failure Rate: "
    f"{failure_rate:.2f}%"
)

# 6. Failure count by payment method
print("\n5. FAILURES BY PAYMENT METHOD")

failure_by_method = (
    df[df["status"] == "FAILED"]
    ["payment_method"]
    .value_counts()
)

print(failure_by_method)

# 7. Failure count by bank
print("\n6. FAILURES BY BANK")

failure_by_bank = (
    df[df["status"] == "FAILED"]
    ["bank"]
    .value_counts()
)

print(failure_by_bank)

# 8. Failure reasons
print("\n7. FAILURE REASONS")

failure_reasons = (
    df[df["status"] == "FAILED"]
    ["error_reason"]
    .value_counts()
)

print(failure_reasons)

# 9. Missing values
print("\n8. MISSING VALUES")

print(df.isnull().sum())

# 10. Incident pattern
print("\n9. POSSIBLE INCIDENT PATTERN")

incident = df[
    (df["payment_method"] == "UPI") &
    (df["bank"] == "Bank_A") &
    (df["error_reason"] == "TIMEOUT")
]

print(f"Matching transactions: {len(incident)}")

print(
    f"Failed among them: "
    f"{(incident['status'] == 'FAILED').sum()}"
)

print("\n" + "=" * 60)
print("DATASET INSPECTION COMPLETE ✅")
print("=" * 60)