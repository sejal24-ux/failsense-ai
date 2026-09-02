import streamlit as st
import requests
import pandas as pd


API_URL = "http://127.0.0.1:8000"


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="FailSense AI",
    page_icon="🚨",
    layout="wide",
)


# ---------------------------------------------------------
# SIMULATION STATE
# ---------------------------------------------------------

if "simulation_started" not in st.session_state:
    st.session_state.simulation_started = False


# ---------------------------------------------------------
# API HELPER
# ---------------------------------------------------------

def get_api(endpoint):

    try:

        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        st.error(
            f"Backend connection failed: {e}"
        )

        return None


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🚨 FailSense AI")

st.caption(
    "Payment Failure Intelligence & Recovery Copilot"
)

st.divider()


# ---------------------------------------------------------
# CONTROL BUTTONS
# ---------------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    if st.button("🔄 Refresh Analysis"):

        st.rerun()


with col2:

    if not st.session_state.simulation_started:

        if st.button(
            "🚨 Run Incident Simulation",
            type="primary"
        ):

            st.session_state.simulation_started = True

            st.rerun()

    else:

        if st.button("↩️ Reset Simulation"):

            st.session_state.simulation_started = False

            st.rerun()


# ---------------------------------------------------------
# SYSTEM STATUS
# ---------------------------------------------------------

if st.session_state.simulation_started:

    st.error(
        "�� INCIDENT SIMULATION ACTIVE"
    )

    st.caption(
        "FailSense AI is replaying a synthetic "
        "payment failure incident."
    )

else:

    st.success(
        "🟢 SYSTEM OPERATING NORMALLY"
    )

    st.caption(
        "No incident is currently being displayed. "
        "Run the simulation to investigate a failure event."
    )


# ---------------------------------------------------------
# LOAD API DATA
# ---------------------------------------------------------

summary = get_api("/summary")


if not summary:

    st.stop()


incidents = get_api("/incidents")

root_cause = get_api("/root-cause")

recovery = get_api("/recovery")

investigation = get_api("/investigation")

transactions = get_api("/transactions")


# ---------------------------------------------------------
# SYSTEM OVERVIEW
# ---------------------------------------------------------

st.subheader("System Overview")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Transactions",
        f"{summary['total_transactions']:,}"
    )


with col2:

    st.metric(
        "Failed Transactions",
        f"{summary['failed_transactions']:,}"
    )


with col3:

    st.metric(
        "Failure Rate",
        f"{summary['failure_rate']:.2f}%"
    )


with col4:

    st.metric(
        "Value at Risk",
        f"₹{summary['transaction_value_at_risk']:,.0f}"
    )


st.divider()


# ---------------------------------------------------------
# TRANSACTION ANALYTICS
# ---------------------------------------------------------

st.subheader("📊 Transaction Analytics")


if transactions:

    transactions_df = pd.DataFrame(
        transactions
    )


    # -----------------------------------------------------
    # PREPARE TIMESTAMP
    # -----------------------------------------------------

    transactions_df["timestamp"] = pd.to_datetime(
        transactions_df["timestamp"]
    )


    # -----------------------------------------------------
    # GRAPH 1 — SUCCESS VS FAILED
    # -----------------------------------------------------

    st.markdown("### Transaction Status")


    status_counts = (
        transactions_df["status"]
        .value_counts()
        .rename_axis("Status")
        .to_frame("Transactions")
    )


    st.bar_chart(
        status_counts
    )


    # -----------------------------------------------------
    # GRAPH 2 — FAILURES BY PAYMENT METHOD
    # -----------------------------------------------------

    st.markdown(
        "### Failed Transactions by Payment Method"
    )


    failed_df = transactions_df[
        transactions_df["status"] == "FAILED"
    ]


    if not failed_df.empty:

        payment_counts = (
            failed_df["payment_method"]
            .value_counts()
            .rename_axis("Payment Method")
            .to_frame("Failed Transactions")
        )


        st.bar_chart(
            payment_counts
        )

    else:

        st.info(
            "No failed transactions available."
        )


    # -----------------------------------------------------
    # GRAPH 3 — FAILURES BY BANK
    # -----------------------------------------------------

    st.markdown(
        "### Failed Transactions by Bank"
    )


    if not failed_df.empty:

        bank_counts = (
            failed_df["bank"]
            .value_counts()
            .rename_axis("Bank")
            .to_frame("Failed Transactions")
        )


        st.bar_chart(
            bank_counts
        )

    else:

        st.info(
            "No failed transactions available."
        )


    # -----------------------------------------------------
    # GRAPH 4 — FAILURE TREND
    # -----------------------------------------------------

    st.markdown(
        "### Failure Trend"
    )


    trend_df = (
        transactions_df
        .set_index("timestamp")
        .resample("5min")
        .agg(
            total_transactions=("status", "count"),
            failed_transactions=(
                "status",
                lambda x: (x == "FAILED").sum()
            )
        )
    )


    if not trend_df.empty:

        st.line_chart(
            trend_df[
                ["failed_transactions"]
            ]
        )

    else:

        st.info(
            "Failure trend unavailable."
        )


    # -----------------------------------------------------
    # TRANSACTION EXPLORER
    # -----------------------------------------------------

    st.divider()

    st.markdown(
        "### 🔎 Transaction Explorer"
    )


    explorer_df = transactions_df.copy()


    # -----------------------------------------------------
    # FILTERS
    # -----------------------------------------------------

    filter_col1, filter_col2, filter_col3 = st.columns(3)


    with filter_col1:

        status_options = ["All"] + sorted(
            explorer_df["status"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )


        selected_status = st.selectbox(
            "Payment Status",
            status_options
        )


    with filter_col2:

        method_options = ["All"] + sorted(
            explorer_df["payment_method"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )


        selected_method = st.selectbox(
            "Payment Method",
            method_options
        )


    with filter_col3:

        bank_options = ["All"] + sorted(
            explorer_df["bank"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )


        selected_bank = st.selectbox(
            "Bank",
            bank_options
        )


    # -----------------------------------------------------
    # APPLY FILTERS
    # -----------------------------------------------------

    if selected_status != "All":

        explorer_df = explorer_df[
            explorer_df["status"].astype(str)
            == selected_status
        ]


    if selected_method != "All":

        explorer_df = explorer_df[
            explorer_df["payment_method"].astype(str)
            == selected_method
        ]


    if selected_bank != "All":

        explorer_df = explorer_df[
            explorer_df["bank"].astype(str)
            == selected_bank
        ]


    st.caption(
        f"Showing {len(explorer_df):,} matching transactions"
    )


    # -----------------------------------------------------
    # TRANSACTION TABLE
    # -----------------------------------------------------

    columns_to_show = [
        "timestamp",
        "status",
        "payment_method",
        "bank",
        "amount"
    ]


    available_columns = [
        col
        for col in columns_to_show
        if col in explorer_df.columns
    ]


    st.dataframe(
        explorer_df[
            available_columns
        ].sort_values(
            "timestamp",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


else:

    st.warning(
        "Transaction data unavailable."
    )


st.divider()


# ---------------------------------------------------------
# HIDE INCIDENT ANALYSIS UNTIL SIMULATION
# ---------------------------------------------------------

if not st.session_state.simulation_started:

    st.info(
        "Incident analysis is hidden until "
        "you run the simulation."
    )

    st.stop()


# ---------------------------------------------------------
# ACTIVE INCIDENT
# ---------------------------------------------------------

st.subheader("🚨 Active Incident")


if incidents and incidents.get("incidents"):

    incident = incidents["incidents"][0]


    col1, col2, col3 = st.columns(3)


    with col1:

        st.error(
            f"Severity: {incident['severity']}"
        )


        st.write(
            f"**Incident ID:** "
            f"{incident['incident_id']}"
        )


        st.write(
            f"**Status:** "
            f"{incident['status']}"
        )


    with col2:

        st.write(
            f"**Incident Window:** "
            f"{incident['start_time']} → "
            f"{incident['end_time']}"
        )


        st.write(
            f"**Affected Transactions:** "
            f"{incident['affected_transactions']:,}"
        )


        st.write(
            f"**Failed Transactions:** "
            f"{incident['failed_transactions']:,}"
        )


    with col3:

        st.write(
            f"**Baseline Failure Rate:** "
            f"{incident['baseline_failure_rate']:.2f}%"
        )


        st.write(
            f"**Incident Failure Rate:** "
            f"{incident['incident_failure_rate']:.2f}%"
        )


        st.write(
            f"**Z-Score:** "
            f"{incident['max_z_score']:.2f}"
        )


else:

    st.success(
        "No active incidents detected."
    )


st.divider()


# ---------------------------------------------------------
# ROOT CAUSE
# ---------------------------------------------------------

st.subheader(
    "🔍 Root Cause Analysis"
)


if root_cause and root_cause.get("root_cause"):

    rc = root_cause["root_cause"]


    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            "### Dominant Failure Pattern"
        )


        st.code(
            rc["fingerprint"]
        )


        st.write(
            f"**Payment Method:** "
            f"{rc['payment_method']}"
        )


        st.write(
            f"**Bank:** "
            f"{rc['bank']}"
        )


        st.write(
            f"**Error Source:** "
            f"{rc['error_source']}"
        )


        st.write(
            f"**Error Step:** "
            f"{rc['error_step']}"
        )


        st.write(
            f"**Error Reason:** "
            f"{rc['error_reason']}"
        )


    with col2:

        st.markdown(
            "### Evidence"
        )


        st.metric(
            "Matching Failures",
            f"{rc['matching_failures']:,}"
        )


        st.metric(
            "Pattern Share",
            f"{rc['pattern_share']:.2f}%"
        )


        st.metric(
            "Confidence",
            f"{rc['confidence']:.2f}%"
        )


        st.info(
            "The root cause is based on the "
            "dominant failure fingerprint inside "
            "the detected incident window."
        )


else:

    st.warning(
        "Root cause unavailable."
    )


st.divider()


# ---------------------------------------------------------
# RECOVERY STRATEGY
# ---------------------------------------------------------

st.subheader(
    "♻️ Recovery Strategy Simulator"
)


if recovery:

    strategies = recovery.get(
        "strategies",
        []
    )


    recommendation = recovery.get(
        "recommendation"
    )


    if strategies:

        recovery_df = pd.DataFrame(
            strategies
        )


        recovery_df = recovery_df.rename(
            columns={
                "strategy":
                    "Strategy",

                "recovery_rate":
                    "Recovery Rate (%)",

                "estimated_recovery":
                    "Estimated Recovery (₹)"
            }
        )


        st.dataframe(
            recovery_df,
            use_container_width=True,
            hide_index=True
        )


        if recommendation:

            st.success(
                f"⭐ Recommended Strategy: "
                f"{recommendation['strategy']}"
            )


            col1, col2 = st.columns(2)


            with col1:

                st.metric(
                    "Estimated Recovery Rate",
                    f"{recommendation['recovery_rate']:.1f}%"
                )


            with col2:

                st.metric(
                    "Estimated Recovered Value",
                    f"₹{recommendation['estimated_recovery']:,.2f}"
                )


    else:

        st.warning(
            "No recovery strategies available."
        )


st.divider()


# ---------------------------------------------------------
# AI INVESTIGATION REPORT
# ---------------------------------------------------------

st.subheader(
    "🤖 AI Investigation Report"
)


if investigation and investigation.get("report"):

    st.code(
        investigation["report"],
        language="text"
    )


else:

    st.warning(
        "Investigation report unavailable."
    )


st.divider()


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.caption(
    "FailSense AI • Prototype using synthetic payment "
    "transaction data • No real-money transactions are processed"
)
