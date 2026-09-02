import pandas as pd

from ml.fingerprint import add_fingerprints
from ml.incident_detector import (
    calculate_time_windows,
    detect_anomalies,
)


def determine_severity(failure_rate, z_score):
    """
    Determine incident severity based on
    failure rate and statistical abnormality.
    """

    if failure_rate >= 20 or z_score >= 8:
        return "CRITICAL"

    if failure_rate >= 10 or z_score >= 5:
        return "HIGH"

    if failure_rate >= 5 or z_score >= 3:
        return "MEDIUM"

    return "LOW"


def create_incidents(df):

    df = df.copy()

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    # Add failure fingerprints
    df = add_fingerprints(df)

    # Calculate time windows
    windows = calculate_time_windows(df)

    # Detect abnormal windows
    windows, baseline = detect_anomalies(
        windows
    )

    abnormal_windows = windows[
        windows["is_anomaly"] == True
    ].copy()

    incidents = []

    if abnormal_windows.empty:
        return incidents

    # Group all abnormal windows
    # into one incident for this MVP

    start_time = abnormal_windows[
        "time_window"
    ].min()

    end_time = abnormal_windows[
        "time_window"
    ].max()

    abnormal_times = set(
        abnormal_windows[
            "time_window"
        ]
    )

    affected_transactions = df[
        df["time_window"].isin(
            abnormal_times
        )
    ]

    failed_transactions = affected_transactions[
        affected_transactions["status"] == "FAILED"
    ]

    # Find dominant fingerprint
    top_fingerprint = (
        failed_transactions[
            "failure_fingerprint"
        ]
        .value_counts()
        .idxmax()
    )

    fingerprint_count = (
        failed_transactions[
            "failure_fingerprint"
        ]
        .value_counts()
        .max()
    )

    # Extract information from fingerprint
    parts = top_fingerprint.split("_")

    payment_method = parts[0]
    bank = parts[1]

    # Calculate average incident failure rate
    incident_failure_rate = (
        affected_transactions["status"]
        .eq("FAILED")
        .mean()
        * 100
    )

    max_z_score = (
        abnormal_windows["z_score"]
        .max()
    )

    severity = determine_severity(
        incident_failure_rate,
        max_z_score
    )

    # Business impact
    transaction_value_at_risk = (
        failed_transactions["amount"]
        .sum()
    )

    incident = {

        "incident_id":
            "INC-2026-001",

        "severity":
            severity,

        "status":
            "ACTIVE",

        "start_time":
            str(start_time),

        "end_time":
            str(end_time),

        "baseline_failure_rate":
            round(baseline, 2),

        "incident_failure_rate":
            round(
                incident_failure_rate,
                2
            ),

        "max_z_score":
            round(
                max_z_score,
                2
            ),

        "payment_method":
            payment_method,

        "bank":
            bank,

        "primary_failure_pattern":
            top_fingerprint,

        "pattern_failure_count":
            int(fingerprint_count),

        "affected_transactions":
            int(len(affected_transactions)),

        "failed_transactions":
            int(len(failed_transactions)),

        "transaction_value_at_risk":
            round(
                transaction_value_at_risk,
                2
            )
    }

    incidents.append(
        incident
    )

    return incidents


if __name__ == "__main__":

    df = pd.read_csv(
        "data/transactions.csv"
    )

    # Create time_window first
    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    df["time_window"] = (
        df["timestamp"]
        .dt.floor("5min")
    )

    incidents = create_incidents(df)

    print("=" * 70)
    print("FAILSENSE AI - INCIDENT MANAGEMENT")
    print("=" * 70)

    if not incidents:

        print(
            "\nNo incidents detected."
        )

    else:

        for incident in incidents:

            print("\n🚨 INCIDENT DETECTED")

            print(
                f"\nIncident ID: "
                f"{incident['incident_id']}"
            )

            print(
                f"Severity: "
                f"{incident['severity']}"
            )

            print(
                f"Status: "
                f"{incident['status']}"
            )

            print(
                f"Start: "
                f"{incident['start_time']}"
            )

            print(
                f"End: "
                f"{incident['end_time']}"
            )

            print(
                f"\nBaseline Failure Rate: "
                f"{incident['baseline_failure_rate']}%"
            )

            print(
                f"Incident Failure Rate: "
                f"{incident['incident_failure_rate']}%"
            )

            print(
                f"Maximum Z-Score: "
                f"{incident['max_z_score']}"
            )

            print(
                f"\nAffected Payment Method: "
                f"{incident['payment_method']}"
            )

            print(
                f"Affected Bank: "
                f"{incident['bank']}"
            )

            print(
                f"\nPrimary Failure Pattern:"
            )

            print(
                incident[
                    "primary_failure_pattern"
                ]
            )

            print(
                f"\nPattern Failure Count: "
                f"{incident['pattern_failure_count']}"
            )

            print(
                f"Affected Transactions: "
                f"{incident['affected_transactions']}"
            )

            print(
                f"Transaction Value at Risk: "
                f"₹{incident['transaction_value_at_risk']:,.2f}"
            )

    print("\n" + "=" * 70)
    print("INCIDENT MANAGEMENT COMPLETE ✅")
    print("=" * 70)