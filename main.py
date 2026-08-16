from modules.report_analyser import analyse_report


# ============================================================
# DISPLAY RESULT
# ============================================================

def display_result(result):

    print("\n==============================================")
    print("          FAILURE PREDICTION")
    print("==============================================")

    print(
        "\nFailure Type:",
        result["failure_type"]
    )

    print(
        "Confidence:",
        str(result["confidence"]) + "%"
    )


    # ========================================================
    # EQUIPMENT
    # ========================================================

    print("\nEquipment:")

    if result["equipment"]:

        for item in result["equipment"]:
            print(" -", item)

    else:

        print(" - Not detected")


    # ========================================================
    # SYMPTOMS
    # ========================================================

    print("\nSymptoms:")

    if result["symptoms"]:

        for item in result["symptoms"]:
            print(" -", item)

    else:

        print(" - Not detected")


    # ========================================================
    # PARTS
    # ========================================================

    print("\nParts:")

    if result["parts"]:

        for item in result["parts"]:
            print(" -", item)

    else:

        print(" - Not detected")


    # ========================================================
    # ACTIONS
    # ========================================================

    print("\nMaintenance Actions:")

    if result["actions"]:

        for item in result["actions"]:
            print(" -", item)

    else:

        print(" - Not detected")


    # ========================================================
    # ROOT CAUSES
    # ========================================================

    print("\nRoot Causes:")

    if result["root_causes"]:

        for item in result["root_causes"]:
            print(" -", item)

    else:

        print(" - Not detected")


# ============================================================
# MAIN PROGRAM
# ============================================================

print("\n==============================================")
print("   INDUSTRIAL MAINTENANCE REPORT ANALYSER")
print("==============================================")

print("\nEnter a maintenance report to analyse.")
print("Type 'exit' to close the program.")


# ============================================================
# CONTINUOUS LOOP
# ============================================================

while True:

    print("\n----------------------------------------------")

    report = input(
        "\nEnter maintenance report:\n> "
    )


    # ========================================================
    # EXIT CONDITION
    # ========================================================

    if report.strip().lower() == "exit":

        print("\n==============================================")
        print("        PROGRAM CLOSED")
        print("==============================================")

        break


    # ========================================================
    # EMPTY INPUT
    # ========================================================

    if not report.strip():

        print(
            "\nPlease enter a maintenance report."
        )

        continue


    # ========================================================
    # ANALYSE REPORT
    # ========================================================

    try:

        result = analyse_report(
            report
        )

        display_result(
            result
        )

    except Exception as e:

        print(
            "\nError while analysing report:"
        )

        print(e)