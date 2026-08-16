import re


# ============================================================
# INDUSTRIAL MAINTENANCE REPORT INFORMATION EXTRACTOR
# ============================================================


def find_keywords(text, keyword_groups):
    """
    Find all matching patterns from a category.
    """

    found = []

    for pattern, display_name in keyword_groups:

        if re.search(pattern, text, re.IGNORECASE):
            found.append(display_name)

    return list(dict.fromkeys(found))


# ============================================================
# EQUIPMENT EXTRACTION
# ============================================================

def extract_equipment(text):

    equipment_patterns = [

        # Pump
        (r"\b(?:pump|pmp)\s*[-_]?\s*[a-z]?\s*[-_]?\s*\d+\b",
         "Pump"),

        # Motor
        (r"\b(?:motor|mtr)\s*[-_]?\s*[a-z]?\s*[-_]?\s*\d+\b",
         "Motor"),

        # Compressor
        (r"\b(?:compressor|comp)\s*[-_]?\s*[a-z]?\s*[-_]?\s*\d+\b",
         "Compressor"),

        # Conveyor
        (r"\bconveyor\s*[-_]?\s*[a-z]?\s*[-_]?\s*\d+\b",
         "Conveyor"),

        # Boiler
        (r"\bboiler\s*[-_]?\s*[a-z]?\s*[-_]?\s*\d+\b",
         "Boiler"),

        # Turbine
        (r"\bturbine\s*[-_]?\s*[a-z]?\s*[-_]?\s*\d+\b",
         "Turbine"),

        # Fan
        (r"\bfan\s*[-_]?\s*[a-z]?\s*[-_]?\s*\d+\b",
         "Fan"),

        # Valve
        (r"\bvalve\s*[-_]?\s*[a-z]?\s*[-_]?\s*\d+\b",
         "Valve"),

        # Generic equipment names without IDs
        (r"\bpump\b", "Pump"),
        (r"\bmotor\b", "Motor"),
        (r"\bcompressor\b", "Compressor"),
        (r"\bconveyor\b", "Conveyor"),
        (r"\bboiler\b", "Boiler"),
        (r"\bturbine\b", "Turbine"),
        (r"\bfan\b", "Fan"),
        (r"\bvalve\b", "Valve"),
    ]

    return find_keywords(
        text,
        equipment_patterns
    )


# ============================================================
# SYMPTOM EXTRACTION
# ============================================================

def extract_symptoms(text):

    symptom_patterns = [

        (r"\bvibration(s)?\b",
         "Excessive vibration"),

        (r"\bshaking\b",
         "Excessive vibration"),

        (r"\boverheat(ed|ing)?\b",
         "Overheating"),

        (r"\bhigh temperature\b",
         "High temperature"),

        (r"\btemperature\s+(increased|increase|rose|rising|high)\b",
         "Increased temperature"),

        (r"\babnormal noise\b",
         "Abnormal noise"),

        (r"\bunusual noise\b",
         "Unusual noise"),

        (r"\bnoise\b",
         "Noise"),

        (r"\blow pressure\b",
         "Low pressure"),

        (r"\bpressure\s+(drop|dropped|decreased|decrease|low)\b",
         "Pressure drop"),

        (r"\bleak(age)?\b",
         "Leakage"),

        (r"\bleaking\b",
         "Leakage"),

        (r"\bstopp(ed|age|ing)?\b",
         "Machine stoppage"),

        (r"\bfail(ed|ure|ing)?\b",
         "Failure"),

        (r"\bcrack(ed)?\b",
         "Crack"),

        (r"\bdamaged\b",
         "Damage"),

        (r"\bbroken\b",
         "Breakage"),

        (r"\bloose\b",
         "Loose connection"),

        (r"\bslipping\b",
         "Slipping"),

        (r"\bslow\b",
         "Slow operation"),

        (r"\bcurrent\s+(increased|increase|high)\b",
         "High current"),

        (r"\bhigh current\b",
         "High current"),

        (r"\bpower loss\b",
         "Power loss"),

        (r"\bshort circuit\b",
         "Short circuit"),
    ]

    return find_keywords(
        text,
        symptom_patterns
    )


# ============================================================
# PART EXTRACTION
# ============================================================

def extract_parts(text):

    part_patterns = [

        (r"\bbearing(s)?\b",
         "Bearing"),

        (r"\bbelt(s)?\b",
         "Belt"),

        (r"\bseal(s)?\b",
         "Seal"),

        (r"\bfilter(s)?\b",
         "Filter"),

        (r"\bcoupling(s)?\b",
         "Coupling"),

        (r"\bvalve(s)?\b",
         "Valve"),

        (r"\bpipe(s)?\b",
         "Pipe"),

        (r"\bterminal(s)?\b",
         "Terminal"),

        (r"\bcable(s)?\b",
         "Cable"),

        (r"\bfuse(s)?\b",
         "Fuse"),

        (r"\bwire(s)?\b",
         "Wire"),

        (r"\bconnection(s)?\b",
         "Electrical connection"),

        (r"\bshaft(s)?\b",
         "Shaft"),

        (r"\bimpeller(s)?\b",
         "Impeller"),

        (r"\bair filter\b",
         "Air filter"),

        (r"\boil\b",
         "Oil"),

        (r"\bgasket(s)?\b",
         "Gasket"),

        (r"\bgear(s)?\b",
         "Gear"),

        (r"\brelay(s)?\b",
         "Relay"),

        (r"\bsensor(s)?\b",
         "Sensor"),

        (r"\bcontactor(s)?\b",
         "Contactor"),

        (r"\bseal ring\b",
         "Seal ring"),
    ]

    return find_keywords(
        text,
        part_patterns
    )


# ============================================================
# ACTION EXTRACTION
# ============================================================

def extract_actions(text):

    action_patterns = [

        # Replacement
        (r"\breplac(e|ed|ing|ement)\b",
         "Replacement"),

        (r"\bchanged\b",
         "Replacement"),

        (r"\bnew\s+\w+\s+(was\s+)?installed\b",
         "Replacement"),

        (r"\binstalled\b",
         "Installation"),

        # Repair
        (r"\brepair(ed|ing)?\b",
         "Repair"),

        (r"\bfix(ed|ing)?\b",
         "Repair"),

        (r"\brestored\b",
         "Restoration"),

        # Inspection
        (r"\binspect(ed|ion|ing)?\b",
         "Inspection"),

        (r"\bchecked\b",
         "Inspection"),

        (r"\btested\b",
         "Testing"),

        # Cleaning
        (r"\bclean(ed|ing)?\b",
         "Cleaning"),

        (r"\bflushed\b",
         "Cleaning"),

        # Adjustment
        (r"\badjust(ed|ment|ing)?\b",
         "Adjustment"),

        (r"\bcalibrat(ed|ion|ing)?\b",
         "Calibration"),

        # Alignment
        (r"\balign(ed|ment|ing)?\b",
         "Alignment"),

        # Lubrication
        (r"\blubricat(ed|ion|ing)?\b",
         "Lubrication"),

        (r"\boiled\b",
         "Oil maintenance"),

        # Shutdown
        (r"\bshutdown\b",
         "Shutdown"),

        (r"\bshut down\b",
         "Shutdown"),

        # Reset
        (r"\breset\b",
         "Reset"),

        # Tightening
        (r"\btighten(ed|ing)?\b",
         "Tightening"),

        # Cooling
        (r"\bcooled\b",
         "Cooling"),

        (r"\bcooling\b",
         "Cooling"),

        # Reconnection
        (r"\breconnect(ed|ing)?\b",
         "Reconnection"),

        # Calibration
        (r"\brecalibrat(ed|ion|ing)?\b",
         "Recalibration"),
    ]

    return find_keywords(
        text,
        action_patterns
    )


# ============================================================
# ROOT CAUSE EXTRACTION
# ============================================================

def extract_root_cause(text):

    patterns = [

        r"because of\s+([^.;]+)",
        r"due to\s+([^.;]+)",
        r"caused by\s+([^.;]+)",
        r"result of\s+([^.;]+)",
        r"as a result of\s+([^.;]+)",
        r"because\s+([^.;]+)",
    ]

    causes = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        for match in matches:

            cause = match.strip()

            if cause:
                causes.append(cause)

    return list(dict.fromkeys(causes))


# ============================================================
# MAIN EXTRACTION FUNCTION
# ============================================================

def extract_information(report):

    if not isinstance(report, str):
        report = str(report)

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        report
    ).strip()

    information = {

        "equipment":
            extract_equipment(text),

        "symptoms":
            extract_symptoms(text),

        "parts":
            extract_parts(text),

        "actions":
            extract_actions(text),

        "root_causes":
            extract_root_cause(text),

    }

    return information


# ============================================================
# TESTING ONLY
# ============================================================

if __name__ == "__main__":

    report = """
    Pump P-101 stopped suddenly because the bearing was worn.
    Excessive vibration and abnormal noise were observed.
    The damaged bearing was replaced and the coupling was
    realigned. The pump was inspected and lubricated.
    """

    result = extract_information(report)

    print("\n========== EXTRACTED INFORMATION ==========\n")

    print("Equipment:")
    print(result["equipment"])

    print("\nSymptoms:")
    print(result["symptoms"])

    print("\nParts:")
    print(result["parts"])

    print("\nActions:")
    print(result["actions"])

    print("\nRoot Causes:")
    print(result["root_causes"])