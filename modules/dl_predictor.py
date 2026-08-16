import os
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)


# ============================================================
# MODEL PATH
# ============================================================

MODEL_PATH = "models/failure_classifier"


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ============================================================
# LOAD TOKENIZER
# ============================================================

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH
)


# ============================================================
# LOAD DEEP LEARNING MODEL
# ============================================================

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

model.to(DEVICE)

model.eval()


# ============================================================
# LOAD LABELS
# ============================================================

LABEL_PATH = os.path.join(
    MODEL_PATH,
    "labels.txt"
)

with open(
    LABEL_PATH,
    "r",
    encoding="utf-8"
) as file:

    labels = [
        line.strip()
        for line in file
        if line.strip()
    ]


# ============================================================
# PREDICT FAILURE TYPE
# ============================================================

def predict_failure_type(report):

    if not isinstance(report, str):
        report = str(report)

    report = report.strip()

    if not report:

        return {
            "failure_type": "Unknown",
            "confidence": 0.0
        }


    # Tokenize report
    inputs = tokenizer(
        report,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )


    # Move input to CPU/GPU
    inputs = {
        key: value.to(DEVICE)
        for key, value in inputs.items()
    }


    # Deep Learning prediction
    with torch.no_grad():

        outputs = model(
            **inputs
        )


    # Convert logits to probabilities
    probabilities = torch.softmax(
        outputs.logits,
        dim=1
    )


    # Highest probability
    confidence, prediction = torch.max(
        probabilities,
        dim=1
    )


    predicted_index = prediction.item()

    confidence_score = confidence.item()


    # Get class name
    if predicted_index < len(labels):

        failure_type = labels[
            predicted_index
        ]

    else:

        failure_type = "Unknown"


    return {

        "failure_type":
            failure_type,

        "confidence":
            round(
                confidence_score * 100,
                2
            )
    }