from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)


# ==========================================================
# DATASET
# ==========================================================

DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "maintenance_reports.csv"
)


def load_data():

    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    return pd.read_csv(DATA_FILE)


# ==========================================================
# DASHBOARD DATA
# ==========================================================

def get_dashboard_data():

    df = load_data()

    # ------------------------------------------------------
    # Failure Type Data
    # ------------------------------------------------------

    failure_data = (
        df["failure_type"]
        .value_counts()
        .reset_index()
    )

    failure_data.columns = [
        "failure_type",
        "count"
    ]

    failure_data = failure_data.to_dict(
        orient="records"
    )


    # ------------------------------------------------------
    # Severity Data
    # ------------------------------------------------------

    severity_data = (
        df["severity"]
        .value_counts()
        .reset_index()
    )

    severity_data.columns = [
        "severity",
        "count"
    ]

    severity_data = severity_data.to_dict(
        orient="records"
    )


    # ------------------------------------------------------
    # Equipment Data
    # ------------------------------------------------------

    equipment_data = []

    if "equipment" in df.columns:

        equipment_data = (
            df["equipment"]
            .value_counts()
            .reset_index()
        )

        equipment_data.columns = [
            "equipment",
            "count"
        ]

        equipment_data = equipment_data.to_dict(
            orient="records"
        )


    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------

    total_reports = len(df)

    total_failures = df["failure_type"].notna().sum()

    critical_reports = (
        df["severity"]
        .astype(str)
        .str.lower()
        .eq("critical")
        .sum()
    )


    return {
        "failure_data": failure_data,
        "severity_data": severity_data,
        "equipment_data": equipment_data,
        "total_reports": total_reports,
        "total_failures": int(total_failures),
        "critical_reports": int(critical_reports)
    }


# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():

    data = get_dashboard_data()

    return render_template(
        "dashboard.html",
        **data
    )


# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/dashboard")
def dashboard():

    data = get_dashboard_data()

    return render_template(
        "dashboard.html",
        **data
    )

@app.route("/api/failure-data")
def failure_data_api():

    data = get_dashboard_data()

    return jsonify(
        data["failure_data"]
    )

@app.route("/api/severity-data")
def severity_data_api():

    data = get_dashboard_data()

    return jsonify(
        data["severity_data"]
    )
# ==========================================================
# ANALYTICS
# ==========================================================

@app.route("/analytics")
def analytics():

    data = get_dashboard_data()

    return render_template(
        "analytics.html",
        **data
    )


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("INDUSTRIAL MAINTENANCE REPORT ANALYZER")
    print("=" * 60)

    print()
    print("Dashboard:")
    print("http://127.0.0.1:5000/dashboard")

    print()
    print("Analytics:")
    print("http://127.0.0.1:5000/analytics")

    print()
    print("=" * 60)

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )