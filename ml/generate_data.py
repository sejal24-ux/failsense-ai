import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# -----------------------------
# Reproducibility
# -----------------------------
random.seed(42)
np.random.seed(42)


# -----------------------------
# Configuration
# -----------------------------
OUTPUT_PATH = "data/transactions.csv"
NUM_TRANSACTIONS = 50_000

payment_methods = [
    "UPI",
    "CARD",
    "NETBANKING",
    "WALLET"
]

banks = [
    "Bank_A",
    "Bank_B",
    "Bank_C",
    "Bank_D",
    "Bank_E"
]

error_sources = [
    "CUSTOMER",
    "BANK",
    "GATEWAY",
    "NETWORK",
    "MERCHANT"
]

error_steps = [
    "INITIATION",
    "AUTHORIZATION",
    "PROCESSING",
    "CONFIRMATION"
]

error_reasons = [
    "TIMEOUT",
    "DECLINED",
    "NETWORK_ERROR",
    "LIMIT_EXCEEDED",
    "INVALID_DETAILS"
]

merchants = [
    f"MERCHANT_{i:03d}"
    for i in range(1, 51)
]

locations = [
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Pune"
]

devices = [
    "Mobile",
    "Desktop",
    "Tablet"
]


# -----------------------------
# Generate transactions
# -----------------------------
start_time = datetime(
    2026,
    8,
    31,
    9,
    0,
    0
)

rows = []

for i in range(NUM_TRANSACTIONS):

    timestamp = start_time + timedelta(
        minutes=random.randint(0, 12 * 60)
    )

    payment_method = random.choices(
        payment_methods,
        weights=[55, 25, 15, 5]
    )[0]

    bank = random.choice(banks)

    amount = round(
        np.random.lognormal(
            mean=7.0,
            sigma=1.0
        ),
        2
    )

    merchant = random.choice(merchants)
    location = random.choice(locations)
    device = random.choice(devices)

    # Normal payment failure probability
    failure_probability = 0.025

    # ----------------------------------------
    # Simulated Bank_A incident
    # UPI + Bank_A + authorization timeout
    # ----------------------------------------
    incident_transaction = (
        payment_method == "UPI"
        and bank == "Bank_A"
        and timestamp.hour == 10
        and 15 <= timestamp.minute <= 45
    )

    if incident_transaction:
        failure_probability = 0.80

    # Determine transaction status
    status = (
        "FAILED"
        if random.random() < failure_probability
        else "SUCCESS"
    )

    # ----------------------------------------
    # Failure information
    # ----------------------------------------
    if status == "FAILED":

        if incident_transaction:

            error_source = "BANK"
            error_step = "AUTHORIZATION"
            error_reason = "TIMEOUT"

        else:

            error_source = random.choice(
                error_sources
            )

            error_step = random.choice(
                error_steps
            )

            error_reason = random.choice(
                error_reasons
            )

        latency = round(
            np.random.uniform(2, 15),
            2
        )

    else:

        error_source = None
        error_step = None
        error_reason = None

        latency = round(
            np.random.uniform(0.5, 4),
            2
        )

    # ----------------------------------------
    # Store transaction
    # ----------------------------------------
    rows.append({

        "transaction_id":
            f"TXN_{i + 1:06d}",

        "timestamp":
            timestamp,

        "merchant_id":
            merchant,

        "amount":
            amount,

        "payment_method":
            payment_method,

        "bank":
            bank,

        "status":
            status,

        "error_source":
            error_source,

        "error_step":
            error_step,

        "error_reason":
            error_reason,

        "latency_seconds":
            latency,

        "location":
            location,

        "device_type":
            device
    })


# -----------------------------
# Create DataFrame
# -----------------------------
df = pd.DataFrame(rows)


# -----------------------------
# Save dataset
# -----------------------------
os.makedirs(
    "data",
    exist_ok=True
)

df.to_csv(
    OUTPUT_PATH,
    index=False
)


# -----------------------------
# Print summary
# -----------------------------
print("=" * 50)
print("FAILSENSE AI DATASET GENERATED")
print("=" * 50)

print(
    f"\nDataset: {OUTPUT_PATH}"
)

print(
    f"Transactions: {len(df)}"
)

print("\nTransaction Status:")
print(
    df["status"].value_counts()
)

print("\nPayment Methods:")
print(
    df["payment_method"].value_counts()
)

failure_rate = (
    df["status"]
    .eq("FAILED")
    .mean()
    * 100
)

print(
    f"\nOverall Failure Rate: "
    f"{failure_rate:.2f}%"
)

print("\nTop Failure Reasons:")
print(
    df.loc[
        df["status"] == "FAILED",
        "error_reason"
    ]
    .value_counts()
    .head()
)

print("\nDataset generation complete! ✅")