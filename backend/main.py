from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import math
import pandas as pd

from ml.fingerprint import add_fingerprints
from ml.incident_detector import (
    calculate_time_windows,
    detect_anomalies,
)
from ml.root_cause import (
    get_incident_transactions,
    calculate_root_cause,
)
from ml.recovery import (
    calculate_recovery_options,
    recommend_strategy,
)
from ml.ai_investigator import (
    build_incident,
    generate_incident_report,
)


app = FastAPI(
    title="FailSense AI",
    description=(
        "Payment Failure Intelligence "
        "and Recovery Copilot"
    ),
    version="1.0.0",
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------

def load_data():

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


# ---------------------------------------------------------
# SAFE JSON CLEANING
# ---------------------------------------------------------

def clean_value(value):

    if value is None:
        return None

    # Handle pandas / numpy missing values
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    # Convert numpy values to normal Python values
    if hasattr(value, "item"):
        try:
            value = value.item()
        except Exception:
            pass

    # Handle float NaN / infinity
    if isinstance(value, float):
        if not math.isfinite(value):
            return None

    return value


def clean_records(records):

    cleaned = []

    for record in records:

        new_record = {}

        for key, value in record.items():

            new_record[key] = clean_value(
                value
            )

        cleaned.append(new_record)

    return cleaned


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.get("/")
def home():

    return {
        "name": "FailSense AI",
        "status": "running",
        "message": (
            "Payment Failure Intelligence API"
        ),
    }


# ---------------------------------------------------------
# TRANSACTIONS
# ---------------------------------------------------------
@app.get("/transactions")
def transactions():

    df = load_data()

    # Return all transactions
    result = df.copy()

    # Convert timestamp to string
    result["timestamp"] = (
        result["timestamp"]
        .astype(str)
    )

    # Convert dataframe to records
    records = result.to_dict(
        orient="records"
    )

    # Remove NaN / infinity values
    records = clean_records(
        records
    )

    return records

# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

@app.get("/summary")
def summary():

    df = load_data()

    total = len(df)

    failures = (
        df["status"] == "FAILED"
    ).sum()

    failure_rate = (
        failures / total * 100
    )

    failed_value = df.loc[
        df["status"] == "FAILED",
        "amount",
    ].sum()

    return {

        "total_transactions":
            int(total),

        "failed_transactions":
            int(failures),

        "failure_rate":
            round(
                float(failure_rate),
                2,
            ),

        "transaction_value_at_risk":
            round(
                float(failed_value),
                2,
            ),
    }


# ---------------------------------------------------------
# INCIDENTS
# ---------------------------------------------------------

@app.get("/incidents")
def incidents():

    df = load_data()

    windows = calculate_time_windows(
        df
    )

    windows, baseline = (
        detect_anomalies(
            windows
        )
    )

    abnormal = windows[
        windows["is_anomaly"] == True
    ]

    if abnormal.empty:

        return {
            "incidents": [],
            "baseline_failure_rate":
                round(
                    float(baseline),
                    2,
                ),
        }

    start_time = (
        abnormal["time_window"]
        .min()
    )

    end_time = (
        abnormal["time_window"]
        .max()
    )

    incident_df = df[
        (df["time_window"] >= start_time)
        &
        (df["time_window"] <= end_time)
    ]

    failures = incident_df[
        incident_df["status"] == "FAILED"
    ]

    # Safety check
    if failures.empty:

        return {
            "incidents": [],
            "baseline_failure_rate":
                round(
                    float(baseline),
                    2,
                ),
        }

    fingerprint_counts = (
        failures[
            "failure_fingerprint"
        ]
        .value_counts()
    )

    dominant_fingerprint = (
        fingerprint_counts.index[0]
    )

    dominant_count = int(
        fingerprint_counts.iloc[0]
    )

    incident_failure_rate = (
        len(failures)
        / len(incident_df)
        * 100
    )

    max_z_score = float(
        abnormal["z_score"].max()
    )

    # -----------------------------------------------------
    # Severity
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # Fingerprint information
    # -----------------------------------------------------

    fingerprint_parts = (
        dominant_fingerprint.split("_")
    )

    payment_method = (
        fingerprint_parts[0]
    )

    if len(fingerprint_parts) > 1:

        bank = "_".join(
            fingerprint_parts[1:-3]
        )

    else:

        bank = "Unknown"

    # -----------------------------------------------------
    # Incident response
    # -----------------------------------------------------

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
            round(
                float(baseline),
                2,
            ),

        "incident_failure_rate":
            round(
                float(incident_failure_rate),
                2,
            ),

        "max_z_score":
            round(
                max_z_score,
                2,
            ),

        "payment_method":
            payment_method,

        "bank":
            bank,

        "failure_pattern":
            dominant_fingerprint,

        "pattern_failure_count":
            dominant_count,

        "affected_transactions":
            int(len(incident_df)),

        "failed_transactions":
            int(len(failures)),

        "transaction_value_at_risk":
            round(
                float(
                    failures["amount"].sum()
                ),
                2,
            ),
    }

    return {
        "incidents": [incident]
    }


# ---------------------------------------------------------
# ROOT CAUSE
# ---------------------------------------------------------

@app.get("/root-cause")
def root_cause():

    df = load_data()

    incident_df, baseline = (
        get_incident_transactions(
            df
        )
    )

    if incident_df is None:

        return {
            "root_cause": None
        }

    result = calculate_root_cause(
        incident_df
    )

    return {
        "root_cause": clean_value(
            result
        )
        if not isinstance(result, dict)
        else {
            key: clean_value(value)
            for key, value in result.items()
        }
    }


# ---------------------------------------------------------
# RECOVERY STRATEGIES
# ---------------------------------------------------------

@app.get("/recovery")
def recovery():

    df = load_data()

    incident_df, baseline = (
        get_incident_transactions(
            df
        )
    )

    if incident_df is None:

        return {
            "strategies": [],
            "recommendation": None,
        }

    results = (
        calculate_recovery_options(
            incident_df
        )
    )

    best = recommend_strategy(
        results
    )

    strategies = (
        results.to_dict(
            orient="records"
        )
    )

    strategies = clean_records(
        strategies
    )

    recommendation = None

    if best is not None:

        recommendation = {
            key: clean_value(value)
            for key, value
            in best.to_dict().items()
        }

    return {

        "strategies":
            strategies,

        "recommendation":
            recommendation,
    }


# ---------------------------------------------------------
# AI INVESTIGATION
# ---------------------------------------------------------

@app.get("/investigation")
def investigation():

    (
        incident,
        root_cause_result,
        recovery_results,
        recommended_strategy,
    ) = build_incident()

    report = generate_incident_report(
        incident,
        root_cause_result,
        recovery_results,
        recommended_strategy,
    )

    return {
        "report": report
    }


# ---------------------------------------------------------
# SERVER TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
