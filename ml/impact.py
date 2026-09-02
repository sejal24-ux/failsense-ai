import pandas as pd

from fingerprint import add_fingerprints


def calculate_business_impact(df):

    df = df.copy()

    # Add fingerprints
    df = add_fingerprints(df)

    # Convert timestamp
    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    # Find failed transactions
    failures = df[
        df["status"] == "FAILED"
    ].copy()

    if failures.empty:
        return {
            "failed_transactions": 0,
            "transaction_value_at_risk": 0,
            "estimated_revenue_at_risk": 0,
            "estimated_recoverable_value": 0
        }

    # Total failed transactions
    failed_transactions = len(failures)

    # Total value of failed transactions
    transaction_value_at_risk = (
        failures["amount"].sum()
    )

    # Prototype assumptions
    #
    # These are simulated estimates.
    # They are NOT actual Razorpay numbers.

    estimated_revenue_at_risk = (
        transaction_value_at_risk * 0.10
    )

    estimated_recoverable_value = (
        transaction_value_at_risk * 0.70
    )

    return {
        "failed_transactions":
            failed_transactions,

        "transaction_value_at_risk":
            round(
                transaction_value_at_risk,
                2
            ),

        "estimated_revenue_at_risk":
            round(
                estimated_revenue_at_risk,
                2
            ),

        "estimated_recoverable_value":
            round(
                estimated_recoverable_value,
                2
            )
    }


if __name__ == "__main__":

    df = pd.read_csv(
        "data/transactions.csv"
    )

    impact = calculate_business_impact(
        df
    )

    print("=" * 70)
    print("FAILSENSE AI - BUSINESS IMPACT ENGINE")
    print("=" * 70)

    print(
        f"\nFailed Transactions: "
        f"{impact['failed_transactions']:,}"
    )

    print(
        f"\nTransaction Value at Risk: "
        f"₹{impact['transaction_value_at_risk']:,.2f}"
    )

    print(
        f"\nEstimated Revenue at Risk: "
        f"₹{impact['estimated_revenue_at_risk']:,.2f}"
    )

    print(
        f"\nEstimated Recoverable Value: "
        f"₹{impact['estimated_recoverable_value']:,.2f}"
    )

    print("\n" + "=" * 70)
    print("BUSINESS IMPACT ANALYSIS COMPLETE ✅")
    print("=" * 70)