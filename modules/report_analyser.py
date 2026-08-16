# ============================================================
# INDUSTRIAL MAINTENANCE REPORT ANALYSER
# NLP + DEEP LEARNING
# ============================================================

from modules.dl_predictor import predict_failure_type
from modules.report_extractor import extract_information


def analyse_report(report):

    # --------------------------------------------------------
    # Validate report
    # --------------------------------------------------------

    if not isinstance(report, str):
        report = str(report)

    report = report.strip()

    if not report:

        return {
            "failure_type": "Unknown",
            "confidence": 0.0,
            "equipment": [],
            "symptoms": [],
            "parts": [],
            "actions": [],
            "root_causes": []
        }


    # ========================================================
    # DEEP LEARNING PREDICTION
    # ========================================================

    prediction = predict_failure_type(report)


    # ========================================================
    # NLP INFORMATION EXTRACTION
    # ========================================================

    extracted = extract_information(report)


    # ========================================================
    # COMBINE RESULTS
    # ========================================================

    return {

        "failure_type":
            prediction["failure_type"],

        "confidence":
            prediction["confidence"],

        "equipment":
            extracted.get("equipment", []),

        "symptoms":
            extracted.get("symptoms", []),

        "parts":
            extracted.get("parts", []),

        "actions":
            extracted.get("actions", []),

        "root_causes":
            extracted.get("root_causes", [])
    }