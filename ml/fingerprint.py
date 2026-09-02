import pandas as pd


def create_failure_fingerprint(row):
    """
    Creates a unique fingerprint for a failed payment.
    """

    if row["status"] != "FAILED":
        return "NO_FAILURE"

    fingerprint = (
        f"{row['payment_method']}_"
        f"{row['bank']}_"
        f"{row['error_source']}_"
        f"{row['error_step']}_"
        f"{row['error_reason']}"
    )

    return fingerprint


def add_fingerprints(df):
    """
    Adds failure fingerprint to every transaction.
    """

    df = df.copy()

    df["failure_fingerprint"] = df.apply(
        create_failure_fingerprint,
        axis=1
    )

    return df


if __name__ == "__main__":

    # Load transaction data
    df = pd.read_csv(
        "data/transactions.csv"
    )

    # Add fingerprints
    df = add_fingerprints(df)

    # Select failed transactions
    failures = df[
        df["status"] == "FAILED"
    ]

    print("=" * 60)
    print("FAILSENSE AI - FAILURE FINGERPRINTING")
    print("=" * 60)

    print("\nTotal transactions:")
    print(len(df))

    print("\nFailed transactions:")
    print(len(failures))

    print("\nTop failure fingerprints:")

    print(
        failures[
            "failure_fingerprint"
        ]
        .value_counts()
        .head(15)
    )

    print("\n" + "=" * 60)
    print("FINGERPRINTING COMPLETE ✅")
    print("=" * 60)