from modules.dl_predictor import predict_failure_type


report = """
Motor M-201 stopped during operation.
The electrical terminal was damaged and
the motor showed abnormal current.
"""


result = predict_failure_type(report)


print("\n========== DEEP LEARNING RESULT ==========\n")

print(
    "Failure Type:",
    result["failure_type"]
)

print(
    "Confidence:",
    str(result["confidence"]) + "%"
)