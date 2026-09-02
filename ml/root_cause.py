import pandas as pd

from ml.fingerprint import add_fingerprints
from ml.incident_detector import (
    calculate_time_windows,
    detect_anomalies,
)


def prepare_data():
    df = pd.read_csv("data/transactions.csv")

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df["time_window"] = df["timestamp"].dt.floor("5min")

    df = add_fingerprints(df)

    return df


def get_incident_transactions(df):
    windows = calculate_time_windows(df)

    windows, baseline = detect_anomalies(windows)

    abnormal_windows = windows[windows["is_anomaly"] == True]

    if abnormal_windows.empty:
        return None, baseline

    start_time = abnormal_windows["time_window"].min()
    end_time = abnormal_windows["time_window"].max()

    incident_transactions = df[
        (df["time_window"] >= start_time) & (df["time_window"] <= end_time)
    ].copy()

    return incident_transactions, baseline


def calculate_root_cause(incident_transactions):
    if incident_transactions is None:
        return None

    failures = incident_transactions[
        incident_transactions["status"] == "FAILED"
    ].copy()

    if failures.empty:
        return None

    fingerprint_counts = failures["failure_fingerprint"].value_counts()

    dominant_fingerprint = fingerprint_counts.index[0]
    dominant_count = int(fingerprint_counts.iloc[0])

    total_failures = len(failures)

    pattern_share = dominant_count / total_failures * 100

    parts = dominant_fingerprint.split("_")

    payment_method = parts[0]

    # Bank names can contain underscores, e.g. Bank_A
    bank = "_".join(parts[1:-3])

    error_source = parts[-3]
    error_step = parts[-2]
    error_reason = parts[-1]

    confidence = min(98, 50 + (pattern_share * 0.6))

    return {
        "fingerprint": dominant_fingerprint,
        "payment_method": payment_method,
        "bank": bank,
        "error_source": error_source,
        "error_step": error_step,
        "error_reason": error_reason,
        "matching_failures": dominant_count,
        "total_failures": total_failures,
        "pattern_share": round(pattern_share, 2),
        "confidence": round(confidence, 2),
    }


def generate_evidence(root_cause):
    if root_cause is None:
        return []

    evidence = []

    evidence.append(
        f"{root_cause['matching_failures']} "
        "incident failures match the dominant "
        "failure fingerprint."
    )

    evidence.append(
        f"The dominant pattern explains "
        f"{root_cause['pattern_share']}% "
        "of failures inside the incident window."
    )

    evidence.append(
        f"The pattern is associated with "
        f"{root_cause['payment_method']} "
        f"transactions involving "
        f"{root_cause['bank']}."
    )

    evidence.append(
        f"The primary error is "
        f"{root_cause['error_reason'].lower()} "
        f"during the "
        f"{root_cause['error_step'].lower()} "
        "stage."
    )

    return evidence


if __name__ == "__main__":
    print("=" * 70)
    print("FAILSENSE AI - INCIDENT-SPECIFIC ROOT CAUSE ANALYSIS")
    print("=" * 70)

    df = prepare_data()

    incident_transactions, baseline = get_incident_transactions(df)

    if incident_transactions is None:
        print("\nNo incident detected.")
    else:
        result = calculate_root_cause(incident_transactions)

        print(f"\nIncident transactions: {len(incident_transactions):,}")
        print(f"Incident failures: {result['total_failures']:,}")

        print("\n🔍 LIKELY ROOT CAUSE")

        print(f"\nPayment Method: {result['payment_method']}")
        print(f"Bank: {result['bank']}")
        print(f"Error Source: {result['error_source']}")
        print(f"Error Step: {result['error_step']}")
        print(f"Error Reason: {result['error_reason']}")

        print(f"\nMatching Failures: {result['matching_failures']}")
        print(f"Pattern Share: {result['pattern_share']}%")

        print(f"\nConfidence Score: {result['confidence']}%")

        print("\nEvidence:")

        evidence = generate_evidence(result)

        for item in evidence:
            print(f"✓ {item}")

        print("\n" + "=" * 70)
        print("ROOT CAUSE ANALYSIS COMPLETE ✅")
        print("=" * 70)