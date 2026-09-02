import pandas as pd

from ml.fingerprint import add_fingerprints
from ml.incident_detector import (
    calculate_time_windows,
    detect_anomalies,
)
from ml.root_cause import calculate_root_cause
from ml.recovery import (
    prepare_data,
    detect_incident,
    calculate_recovery_options,
    recommend_strategy,
)


def generate_incident_report(
    incident,
    root_cause,
    recovery_results,
    recommended_strategy,
):
    """
    Generate a human-readable incident investigation report.

    This is the deterministic AI-report prototype.
    Later we can connect an LLM to this structured output.
    """

    if incident is None:
        return "No active incident detected."

    report = f"""
============================================================
FAILSENSE AI — INCIDENT INVESTIGATION REPORT
============================================================

🚨 INCIDENT SUMMARY

Incident ID:
{incident['incident_id']}

Severity:
{incident['severity']}

Status:
{incident['status']}

Incident Window:
{incident['start_time']} → {incident['end_time']}


------------------------------------------------------------
1. WHAT HAPPENED?
------------------------------------------------------------

The payment system detected an abnormal increase
in payment failures during the incident window.

Normal failure rate:
{incident['baseline_failure_rate']}%

Observed incident failure rate:
{incident['incident_failure_rate']}%

Maximum anomaly score:
{incident['max_z_score']}


------------------------------------------------------------
2. WHAT WAS AFFECTED?
------------------------------------------------------------

Payment Method:
{incident['payment_method']}

Bank:
{incident['bank']}

Affected Transactions:
{incident['affected_transactions']}

Failed Transactions:
{incident['failed_transactions']}


------------------------------------------------------------
3. LIKELY ROOT CAUSE
------------------------------------------------------------

Primary Failure Pattern:
{incident['primary_failure_pattern']}

Matching Failures:
{incident['pattern_failure_count']}

Root Cause Confidence:
{root_cause['confidence']}%

Pattern Share:
{root_cause['pattern_share']}%

Likely Explanation:

The dominant failure pattern indicates that
{root_cause['payment_method']} transactions involving
{root_cause['bank']} were experiencing
{root_cause['error_reason'].lower()} errors during
the {root_cause['error_step'].lower()} stage.


------------------------------------------------------------
4. BUSINESS IMPACT
------------------------------------------------------------

Transaction Value at Risk:
₹{incident['transaction_value_at_risk']:,.2f}

This represents the transaction value associated
with failed transactions during the detected incident.


------------------------------------------------------------
5. RECOVERY OPTIONS
------------------------------------------------------------
"""

    for _, row in recovery_results.iterrows():

        report += f"""

{row['strategy']}

Estimated Recovery Rate:
{row['recovery_rate']:.1f}%

Estimated Recovered Value:
₹{row['estimated_recovery']:,.2f}
"""

    report += f"""

------------------------------------------------------------
6. RECOMMENDED ACTION
------------------------------------------------------------

⭐ {recommended_strategy['strategy']}

Estimated Recovery Rate:
{recommended_strategy['recovery_rate']:.1f}%

Estimated Recovered Value:
₹{recommended_strategy['estimated_recovery']:,.2f}


------------------------------------------------------------
7. WHY THIS ACTION?
------------------------------------------------------------

The recommended strategy has the highest estimated
recovery among the simulated intervention strategies.

These recovery values are prototype estimates generated
from simulated transaction data and should not be treated
as actual payment-provider performance guarantees.


------------------------------------------------------------
8. IMPORTANT LIMITATIONS
------------------------------------------------------------

• Transaction data is simulated.
• Recovery rates are prototype estimates.
• Root-cause confidence is a heuristic score.
• The system does not process real payments.
• The system does not perform actual payment routing.
• Production deployment would require real-time payment,
  bank and gateway telemetry.


============================================================
END OF INCIDENT REPORT
============================================================
"""

    return report


def build_incident():

    # Prepare transaction data
    df = prepare_data()

    # Detect incident
    incident_data = detect_incident(df)

    if incident_data is None:
        return None, None, None, None

    incident_transactions = (
        incident_data["transactions"]
    )

    failures = incident_transactions[
        incident_transactions["status"] == "FAILED"
    ]

    # Determine dominant fingerprint
    fingerprint_counts = (
        failures["failure_fingerprint"]
        .value_counts()
    )

    dominant_fingerprint = (
        fingerprint_counts.index[0]
    )

    pattern_count = (
        fingerprint_counts.iloc[0]
    )

    # Calculate incident failure rate
    incident_failure_rate = (
        len(failures)
        / len(incident_transactions)
        * 100
    )

    # Maximum anomaly
    windows = calculate_time_windows(df)

    windows, baseline = detect_anomalies(
        windows
    )

    abnormal_windows = windows[
        windows["is_anomaly"]
    ]

    max_z_score = (
        abnormal_windows["z_score"]
        .max()
    )

    # Incident severity
    if (
        incident_failure_rate >= 20
        or max_z_score >= 8
    ):
        severity = "CRITICAL"

    elif (
        incident_failure_rate >= 10
        or max_z_score >= 5
    ):
        severity = "HIGH"

    elif (
        incident_failure_rate >= 5
        or max_z_score >= 3
    ):
        severity = "MEDIUM"

    else:
        severity = "LOW"

    # Extract dominant pattern
    parts = dominant_fingerprint.split("_")

    payment_method = parts[0]
    bank = parts[1]

    # Create incident object
    incident = {

        "incident_id":
            "INC-2026-001",

        "severity":
            severity,

        "status":
            "ACTIVE",

        "start_time":
            str(
                incident_data["start_time"]
            ),

        "end_time":
            str(
                incident_data["end_time"]
            ),

        "baseline_failure_rate":
            round(
                baseline,
                2
            ),

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
            dominant_fingerprint,

        "pattern_failure_count":
            int(pattern_count),

        "affected_transactions":
            int(
                len(
                    incident_transactions
                )
            ),

        "failed_transactions":
            int(
                len(failures)
            ),

        "transaction_value_at_risk":
            round(
                failures["amount"].sum(),
                2
            )
    }

    # Root cause
    root_cause = calculate_root_cause(
        df
    )

    # Recovery
    recovery_results = (
        calculate_recovery_options(
            incident_transactions
        )
    )

    recommended_strategy = (
        recommend_strategy(
            recovery_results
        )
    )

    return (
        incident,
        root_cause,
        recovery_results,
        recommended_strategy,
    )


if __name__ == "__main__":

    (
        incident,
        root_cause,
        recovery_results,
        recommended_strategy,
    ) = build_incident()

    print(
        "\nGenerating incident investigation...\n"
    )

    report = generate_incident_report(
        incident,
        root_cause,
        recovery_results,
        recommended_strategy,
    )

    print(report)