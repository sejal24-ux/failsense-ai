import pandas as pd
import numpy as np

from ml.fingerprint import add_fingerprints


def calculate_time_windows(df):
    """
    Divide transactions into 5-minute windows
    and calculate failure rate for each window.
    """

    df = df.copy()

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    df["time_window"] = (
        df["timestamp"]
        .dt.floor("5min")
    )

    result = (
        df.groupby("time_window")
        .agg(
            total_transactions=(
                "transaction_id",
                "count"
            ),

            failed_transactions=(
                "status",
                lambda x: (x == "FAILED").sum()
            )
        )
        .reset_index()
    )

    result["failure_rate"] = (
        result["failed_transactions"]
        / result["total_transactions"]
        * 100
    )

    return result


def detect_anomalies(window_df):
    """
    Detect unusually high failure-rate windows
    using a statistical z-score.
    """

    df = window_df.copy()

    baseline = df["failure_rate"].median()

    std = df["failure_rate"].std()

    if std == 0 or pd.isna(std):
        std = 0.01

    df["z_score"] = (
        df["failure_rate"] - baseline
    ) / std

    # 3 standard deviations above baseline
    df["is_anomaly"] = (
        df["z_score"] >= 3
    )

    return df, baseline


def get_incident_patterns(df):
    """
    Find fingerprints that become unusually frequent
    during abnormal time windows.
    """

    df = df.copy()

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    df["time_window"] = (
        df["timestamp"]
        .dt.floor("5min")
    )

    windows = calculate_time_windows(df)

    analyzed_windows, baseline = detect_anomalies(
        windows
    )

    abnormal_windows = analyzed_windows[
        analyzed_windows["is_anomaly"]
    ]

    if abnormal_windows.empty:
        return analyzed_windows, pd.DataFrame()

    abnormal_times = set(
        abnormal_windows["time_window"]
    )

    abnormal_transactions = df[
        df["time_window"].isin(
            abnormal_times
        )
    ]

    failures = abnormal_transactions[
        abnormal_transactions["status"] == "FAILED"
    ]

    fingerprint_counts = (
        failures[
            "failure_fingerprint"
        ]
        .value_counts()
        .reset_index()
    )

    fingerprint_counts.columns = [
        "failure_fingerprint",
        "failure_count"
    ]

    return analyzed_windows, fingerprint_counts


if __name__ == "__main__":

    # Load data
    df = pd.read_csv(
        "data/transactions.csv"
    )

    # Add fingerprints
    df = add_fingerprints(df)

    print("=" * 70)
    print("FAILSENSE AI - INCIDENT DETECTION ENGINE")
    print("=" * 70)

    # Analyze time windows
    windows, baseline = detect_anomalies(
        calculate_time_windows(df)
    )

    print(
        f"\nNormal baseline failure rate: "
        f"{baseline:.2f}%"
    )

    print("\nHighest failure-rate windows:")

    print(
        windows
        .sort_values(
            "failure_rate",
            ascending=False
        )
        .head(10)
        .to_string(index=False)
    )

    # Find incidents
    analyzed, patterns = get_incident_patterns(
        df
    )

    print("\n" + "=" * 70)
    print("POTENTIAL INCIDENT WINDOWS")
    print("=" * 70)

    incidents = analyzed[
        analyzed["is_anomaly"]
    ]

    if incidents.empty:

        print(
            "\nNo abnormal incident detected."
        )

    else:

        print(
            incidents.to_string(
                index=False
            )
        )

    print("\n" + "=" * 70)
    print("FAILURE PATTERNS DURING INCIDENTS")
    print("=" * 70)

    if patterns.empty:

        print(
            "\nNo dominant failure pattern found."
        )

    else:

        print(
            patterns.head(10)
            .to_string(index=False)
        )

    print("\n" + "=" * 70)
    print("INCIDENT DETECTION COMPLETE ✅")
    print("=" * 70)