# Subscription Billing & Status Evaluation Engine

## Project Overview

The Subscription Billing & Status Evaluation Engine is a Python-based system that processes subscription and usage data to calculate monthly bills, apply business rules, evaluate subscription status, and generate billing reports.

The application also provides a web dashboard using Flask for visual insights and supports unit testing with structured coverage.

---

## Tech Stack

- Python 3.11+
- Flask
- Pandas
- Chart.js
- unittest
- Python Logging Module

---


## Business Rules

### Usage Aggregation
- Only usage records for March 2024 are considered.
- Invalid dates are ignored.
- If no usage exists, usage defaults to 0.

### Billing Rules
- If usage ≤ usage_limit_gb → total_bill = monthly_fee
- If usage > usage_limit_gb:
  - overage_gb = usage - usage_limit_gb
  - overage_charge = overage_gb × 10
  - total_bill = monthly_fee + overage_charge
- If status = SUSPENDED → charge only monthly_fee
- If status = CANCELLED → bill = 0

### Status Evaluation
- If usage > 150% of limit → final_status = SUSPENDED
- If previously SUSPENDED and usage ≤ limit → ACTIVE
- CANCELLED status never changes

---

## Installation

### 1. Clone Repository

```
git clone <your-repository-url>
cd Subscription-Billing
```

### 2. Create Virtual Environment (Recommended)

```
python -m venv venv
```

Activate it:

**Windows**
```
venv\Scripts\activate
```

**Mac/Linux**
```
source venv/bin/activate
```

### 3. Install Dependencies

If requirements.txt exists:

```
pip install -r requirements.txt
```

Otherwise install manually:

```
pip install flask pandas
```

---

## Running the Application

```
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

Upload:
- subscriptions.csv
- usage.csv

The system will:
- Process billing
- Generate billing_output.csv
- Generate billing_summary.json
- Display dashboard insights

---

## Running Unit Tests

Run all tests:

```
python -m unittest discover tests
```

Run specific test file:

```
python -m unittest tests/test_billing_engine.py
```

---

## Output Files

### billing_output.csv
Contains:
- subscription_id
- customer_id
- plan
- total_usage_gb
- overage_gb
- total_bill
- final_status

### billing_summary.json
Contains:
- total_subscriptions
- active_subscriptions
- suspended_subscriptions
- cancelled_subscriptions
- total_revenue
- average_bill

---

## Logging

Logs are stored in:

```
logs/billing.log
```

The application handles invalid data safely and logs errors without crashing.

---

## Assumptions

- Only March 2024 usage is processed
- Missing usage defaults to 0
- Overage rate is fixed at $10 per GB
- Cancelled subscriptions are not billed

---

## Edge Cases Handled

- No usage records
- Invalid dates
- Missing numeric values
- Suspended-to-active transitions
- Cancelled subscriptions

---

## Evaluation Criteria Covered

- Modular code structure
- Proper separation of concerns
- Business rules correctly implemented
- Logging implemented
- Unit tests with structured coverage
- Clean and maintainable code

---