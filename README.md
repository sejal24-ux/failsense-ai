# FailSense AI

### AI-Powered Payment Failure Intelligence & Recovery Copilot

FailSense AI is a prototype system that analyzes payment transaction failures, detects abnormal failure incidents, identifies probable root causes, estimates business impact, and recommends recovery strategies.

The system is designed as an explainable payment-failure intelligence and decision-support layer rather than a payment processing system.

---

## Problem Statement

Payment failures can occur because of bank authorization issues, payment-method problems, timeouts, or other recurring failure patterns.

A simple failure counter can show that payments are failing, but it does not answer important operational questions:

- What is causing the failures?
- Is the failure rate abnormal?
- Which payment method or bank is affected?
- How severe is the incident?
- How many transactions are affected?
- How much transaction value is at risk?
- Which recovery strategy could potentially recover the most value?

FailSense AI addresses these questions through an end-to-end payment failure intelligence pipeline.

---

## Key Features

- Payment transaction analytics
- Failure fingerprint generation
- Time-window anomaly detection
- Payment incident detection
- Incident severity classification
- Root cause analysis
- Root cause confidence estimation
- Failure pattern share analysis
- Transaction value-at-risk estimation
- Recovery strategy simulation
- Recovery strategy recommendation
- AI investigation report
- Interactive Streamlit dashboard
- FastAPI backend
- Transaction Explorer with filters
- Incident simulation workflow
- Reset simulation workflow
- REST API endpoints

---

## System Workflow

```text
Payment Transaction Data
          |
          v
Data Processing
          |
          v
Failure Fingerprinting
          |
          v
Time-Window Anomaly Detection
          |
          v
Incident Detection
          |
          v
Severity Classification
          |
          v
Root Cause Analysis
          |
          v
Business Impact Analysis
          |
          v
Recovery Strategy Simulation
          |
          v
Best Strategy Recommendation
          |
          v
AI Investigation Report
          |
          v
Streamlit Dashboard
System Architecture

                    +----------------------+
                    |   Transaction Data   |
                    |  transactions.csv    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |   ML / Analytics     |
                    |                      |
                    | Failure Fingerprint  |
                    | Anomaly Detection    |
                    | Incident Detection   |
                    | Root Cause Analysis  |
                    | Impact Analysis      |
                    | Recovery Strategy    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |    FastAPI Backend   |
                    |      REST APIs       |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Streamlit Dashboard  |
                    |                      |
                    | System Overview      |
                    | Transaction Analytics|
                    | Transaction Explorer |
                    | Incident Analysis    |
                    | Recovery Simulator   |
                    | AI Investigation     |
                    +----------------------+
Project Structure

failsense-ai/
|
├── backend/
│   └── main.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   └── transactions.csv
│
├── ml/
│   ├── __init__.py
│   ├── ai_investigator.py
│   ├── fingerprint.py
│   ├── generate_data.py
│   ├── impact.py
│   ├── incident.py
│   ├── incident_detector.py
│   ├── inspect_data.py
│   ├── recovery.py
│   ├── root_cause.py
│   └── strategy_engine.py
│
├── tests/
│
├── docs/
│
├── screenshots/
│   ├── 01_system_overview.png
│   ├── 02_transaction_analytics.png
│   ├── 03_active_incident.png
│   ├── 04_root_cause_analysis.png
│   ├── 05_recovery_strategy.png
│   ├── 06_ai_investigation_report_top.png
│   ├── 07_ai_investigation_report_middle.png
│   └── 08_ai_investigation_report_bottom.png
│
├── .gitignore
├── requirements.txt
└── README.md
Technology Stack
Programming Language
Python

Backend
FastAPI

Uvicorn

Data Processing
Pandas

NumPy

Machine Learning / Intelligence
Anomaly detection

Failure pattern analysis

Incident detection

Root cause analysis

Business impact analysis

Recovery strategy simulation

Decision-support logic

Dashboard
Streamlit

Data visualization

Development Tools
Git

GitHub

VS Code

Python Virtual Environment

Core Components
1. Transaction Analytics
The system analyzes payment transactions using attributes such as:

Timestamp

Payment status

Payment method

Bank

Failure reason

Transaction amount

The dashboard provides an overview of transaction behavior and failure distribution.

2. Failure Fingerprinting
Failed transactions are converted into structured failure patterns using relevant transaction attributes.

A failure fingerprint can combine:


Payment Method
+
Bank
+
Failure Reason
Example:


UPI_Bank_A_BANK_AUTHORIZATION_TIMEOUT
This allows recurring failure patterns to be identified and analyzed.

3. Time-Window Anomaly Detection
The system analyzes payment failures over time windows.

It compares the observed failure rate with the normal failure rate to identify abnormal increases.

This helps distinguish normal payment failures from potential incidents.

4. Incident Detection
When abnormal behavior crosses predefined conditions, the system creates an incident.

An incident contains information such as:

Incident ID

Incident status

Incident time window

Normal failure rate

Observed failure rate

Anomaly score

Affected transactions

Failed transactions

Payment method

Bank

Example:


Incident ID: INC-2026-001
Status: ACTIVE
Severity: HIGH
5. Incident Severity Classification
Detected incidents are classified according to the scale of the anomaly and its potential business impact.

Possible severity levels include:

LOW

MEDIUM

HIGH

CRITICAL

This helps prioritize operational response.

6. Root Cause Analysis
The system analyzes failure patterns within an incident to identify the dominant probable cause.

The analysis considers:

Failure pattern

Matching failure count

Pattern share

Root cause confidence

Example:


Primary Failure Pattern:
UPI_Bank_A_BANK_AUTHORIZATION_TIMEOUT
The system also provides a confidence estimate rather than presenting the root cause as absolute certainty.

7. Business Impact Analysis
FailSense AI estimates the transaction value affected by an incident.

The key metric is:


Transaction Value at Risk
This provides a business-oriented view of the incident rather than focusing only on the number of failed transactions.

8. Recovery Strategy Simulation
The system simulates different possible recovery strategies.

Current strategies include:

Do Nothing

Retry After Delay

Offer Alternative Payment

Dynamic Routing

Each strategy is associated with a prototype recovery estimate.

The system estimates:


Potential Recovery Rate
+
Estimated Recoverable Transaction Value
The strategy with the highest estimated recovery impact can then be recommended.

9. AI Investigation Report
The investigation layer combines multiple outputs into a structured operational report.


Incident
   +
Root Cause
   +
Confidence
   +
Business Impact
   +
Recovery Recommendation
The resulting report provides a concise summary of the incident and the recommended response.

Dashboard
The FailSense AI dashboard provides an interactive interface for monitoring transactions, investigating incidents, analyzing root causes, and comparing recovery strategies.

System Overview
The System Overview provides a high-level view of payment system health, including transaction volume, failure metrics, and system status.

System Overview

Transaction Analytics
Transaction Analytics provides visual insights into transaction status, payment-method failures, bank-level failures, and transaction-level exploration.

Transaction Analytics

The Transaction Explorer allows users to filter transactions by:

Payment Status

Payment Method

Bank

Active Incident
The Active Incident section displays detected incidents with severity, incident status, affected transactions, failure rate, and incident window.

Active Incident

Root Cause Analysis
The Root Cause Analysis section identifies the dominant probable failure pattern and provides supporting confidence and pattern-share metrics.

Root Cause Analysis

Recovery Strategy Simulator
The Recovery Strategy Simulator compares possible recovery actions and estimates their potential recovery impact.

Recovery Strategy

The simulator compares:

Do Nothing

Retry After Delay

Offer Alternative Payment

Dynamic Routing

The system recommends the strategy with the highest estimated recovery impact.

AI Investigation Report
The AI Investigation Report combines incident detection, root-cause analysis, business impact, and recovery recommendations into a structured investigation.

Investigation Report — Top
AI Investigation Report Top

Investigation Report — Middle
AI Investigation Report Middle

Investigation Report — Bottom
AI Investigation Report Bottom

Incident Analysis Workflow
The incident analysis section becomes available after running the incident simulation.

It displays:

Active Incident

Root Cause Analysis

Recovery Strategy Simulator

AI Investigation Report

The analysis can also be reset using the Reset Simulation option.

API Endpoints
The FastAPI backend provides REST endpoints for different components of the system.


GET /summary
GET /transactions
GET /incidents
GET /root-cause
GET /recovery
GET /investigation
The Streamlit dashboard communicates with the backend through these APIs.

Running the Project
1. Clone the Repository
Bash

git clone https://github.com/sejal24-ux/failsense-ai.git
cd failsense-ai
2. Create a Virtual Environment
Bash

python3 -m venv venv
3. Activate the Virtual Environment
macOS / Linux
Bash

source venv/bin/activate
Windows
Bash

venv\Scripts\activate
4. Install Dependencies
Bash

pip install -r requirements.txt
5. Start the FastAPI Backend
Bash

uvicorn backend.main:app --reload
The backend will run at:


http://127.0.0.1:8000
6. Start the Streamlit Dashboard
Open a second terminal.

Navigate to the project directory:

Bash

cd failsense-ai
Activate the virtual environment:

Bash

source venv/bin/activate
Then run:

Bash

streamlit run dashboard/app.py
The Streamlit dashboard will open in the browser.

Example Investigation Output
An example prototype investigation may look like:


Incident ID: INC-2026-001

Severity:
HIGH

Status:
ACTIVE

Primary Failure Pattern:
UPI_Bank_A_BANK_AUTHORIZATION_TIMEOUT

Root Cause Confidence:
57.73%

Transaction Value at Risk:
₹400,717.56

Recommended Recovery Strategy:
Dynamic Routing
These values are generated from the project's synthetic transaction dataset and recovery simulation.

Example Recovery Comparison
Strategy	Recovery Rate
Do Nothing	25%
Retry After Delay	40%
Offer Alternative Payment	55%
Dynamic Routing	65%

The system recommends the strategy with the highest estimated recovery impact.

Data
The project currently uses a synthetic payment transaction dataset.

The dataset contains transaction-level information required for:

Failure analysis

Pattern detection

Incident simulation

Root cause analysis

Business impact estimation

Recovery simulation

No real customer payment data is used.

Important Disclaimer
FailSense AI is a prototype built using synthetic payment transaction data.

It does not:

Process real payments

Move real money

Perform live payment routing

Interact with real banks

Make production payment decisions

Recovery percentages and business impact values are prototype simulation outputs and should not be interpreted as real-world payment performance measurements.

Design Principles
Explainability
The system attempts to show why an incident was detected and what failure pattern contributed to it.

Decision Support
The system provides recovery recommendations rather than directly executing payment actions.

Business Impact
The system considers transaction value at risk in addition to failure counts.

Uncertainty Awareness
Root cause analysis includes a confidence estimate instead of treating every prediction as certain.

Human Oversight
The prototype is designed as a decision-support system where operational decisions can remain under human control.

Future Improvements
Potential future improvements include:

Real-time transaction streaming

Production-grade anomaly detection models

Online learning

More advanced causal root cause analysis

Confidence-aware human escalation

Historical incident comparison

Automated incident notifications

Real payment gateway integration

Model monitoring

Model drift detection

Production deployment

Authentication

Role-based access control

Persistent incident history

Advanced recovery optimization

Learning Outcomes
This project demonstrates practical experience with:

Python backend development

REST API development

Data analysis

Anomaly detection

Failure pattern analysis

Incident management concepts

Root cause analysis

Business impact estimation

Decision-support systems

Streamlit dashboard development

Git and GitHub workflow

Author
Sejal Kumari

GitHub:
https://github.com/sejal24-ux

Project Status
Status: Prototype / Academic & Portfolio Project

Built for demonstrating payment failure intelligence, analytics, incident investigation, and recovery decision-support capabilities.

