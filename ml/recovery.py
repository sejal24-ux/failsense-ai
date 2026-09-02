import pandas as pd

from ml.fingerprint import add_fingerprints
from ml.incident_detector import (
    calculate_time_windows,
    detect_anomalies,
)


def prepare_data():

    df = pd.read_csv(
        "data/transactions.csv"
    )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    df["time_window"] = (
        df["timestamp"]
        .dt.floor("5min")
    )

    df = add_fingerprints(df)

    return df


def detect_incident(df):

    # Calculate failure rates
    windows = calculate_time_windows(df)

    # Detect abnormal windows
    windows, baseline = detect_anomalies(
        windows
    )

    abnormal_windows = windows[
        windows["is_anomaly"] == True
    ]

    if abnormal_windows.empty:
        return None

    # Get incident time range
    start_time = abnormal_windows[
        "time_window"
    ].min()

    end_time = abnormal_windows[
        "time_window"
    ].max()

    # Select transactions inside incident
    incident_transactions = df[
        (df["time_window"] >= start_time)
        &
        (df["time_window"] <= end_time)
    ].copy()

    return {
        "start_time": start_time,
        "end_time": end_time,
        "baseline": baseline,
        "transactions": incident_transactions
    }


def calculate_recovery_options(
    incident_transactions
):

    failures = incident_transactions[
        incident_transactions["status"]
        == "FAILED"
    ].copy()

    if failures.empty:
        return pd.DataFrame()

    # Value affected by THIS incident
    value_at_risk = failures[
        "amount"
    ].sum()

    # Prototype recovery assumptions.
    # These are simulated estimates.

    strategies = [

        {
            "strategy":
                "Do Nothing",

            "recovery_rate":
                0.25
        },

        {
            "strategy":
                "Retry After Delay",

            "recovery_rate":
                0.40
        },

        {
            "strategy":
                "Offer Alternative Payment",

            "recovery_rate":
                0.55
        },

        {
            "strategy":
                "Dynamic Routing",

            "recovery_rate":
                0.65
        }
    ]

    results = []

    for strategy in strategies:

        estimated_recovery = (
            value_at_risk
            * strategy["recovery_rate"]
        )

        results.append({

            "strategy":
                strategy["strategy"],

            "recovery_rate":
                strategy["recovery_rate"] * 100,

            "estimated_recovery":
                round(
                    estimated_recovery,
                    2
                )
        })

    return pd.DataFrame(results)


def recommend_strategy(
    recovery_df
):

    if recovery_df.empty:
        return None

    best_index = recovery_df[
        "estimated_recovery"
    ].idxmax()

    return recovery_df.loc[
        best_index
    ]


if __name__ == "__main__":

    print("=" * 70)
    print(
        "FAILSENSE AI - INCIDENT-SPECIFIC "
        "RECOVERY SIMULATOR"
    )
    print("=" * 70)

    # Prepare data
    df = prepare_data()

    # Detect incident
    incident = detect_incident(df)

    if incident is None:

        print(
            "\nNo incident detected."
        )

    else:

        incident_transactions = (
            incident["transactions"]
        )

        failures = incident_transactions[
            incident_transactions["status"]
            == "FAILED"
        ]

        print(
            f"\nIncident Start: "
            f"{incident['start_time']}"
        )

        print(
            f"Incident End: "
            f"{incident['end_time']}"
        )

        print(
            f"\nIncident Transactions: "
            f"{len(incident_transactions):,}"
        )

        print(
            f"Failed Transactions: "
            f"{len(failures):,}"
        )

        value_at_risk = failures[
            "amount"
        ].sum()

        print(
            f"Transaction Value at Risk: "
            f"₹{value_at_risk:,.2f}"
        )

        # Recovery simulation
        recovery_results = (
            calculate_recovery_options(
                incident_transactions
            )
        )

        print(
            "\n" + "=" * 70
        )

        print(
            "RECOVERY STRATEGIES"
        )

        print("=" * 70)

        print(
            recovery_results.to_string(
                index=False
            )
        )

        # Best strategy
        best = recommend_strategy(
            recovery_results
        )

        if best is not None:

            print(
                "\n" + "=" * 70
            )

            print(
                "⭐ RECOMMENDED ACTION"
            )

            print("=" * 70)

            print(
                f"\nStrategy: "
                f"{best['strategy']}"
            )

            print(
                f"Estimated Recovery Rate: "
                f"{best['recovery_rate']:.1f}%"
            )

            print(
                f"Estimated Recovered Value: "
                f"₹{best['estimated_recovery']:,.2f}"
            )

    print(
        "\n" + "=" * 70
    )

    print(
        "INCIDENT RECOVERY SIMULATION COMPLETE ✅"
    )

    print(
        "=" * 70
    )