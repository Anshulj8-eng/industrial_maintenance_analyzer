import os
import pandas as pd
import numpy as np
import torch

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)


# ============================================================
# CONFIGURATION
# ============================================================

DATA_PATH = "data/maintenance_reports.csv"

MODEL_NAME = "distilbert-base-uncased"

MODEL_OUTPUT_DIR = "models/failure_classifier"

MAX_LENGTH = 128

TEST_SIZE = 0.2

RANDOM_STATE = 42


# ============================================================
# CHECK DEVICE
# ============================================================

device = "cuda" if torch.cuda.is_available() else "cpu"

print("\n========================================")
print(" INDUSTRIAL MAINTENANCE DL TRAINING")
print("========================================")

print("\nDevice:", device)

if device == "cuda":
    print("GPU detected.")
else:
    print("GPU not detected. Training will use CPU.")


# ============================================================
# LOAD DATASET
# ============================================================

print("\nLoading dataset...")

if not os.path.exists(DATA_PATH):

    raise FileNotFoundError(
        f"\nDataset not found:\n{DATA_PATH}\n"
        "Make sure the CSV is inside the data folder."
    )

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully.")

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "report_text",
    "failure_type"
]

for column in required_columns:

    if column not in df.columns:

        raise ValueError(
            f"\nRequired column '{column}' is missing."
            f"\nAvailable columns: {df.columns.tolist()}"
        )


# ============================================================
# CLEAN DATA
# ============================================================

df = df[
    ["report_text", "failure_type"]
].copy()

df["report_text"] = (
    df["report_text"]
    .fillna("")
    .astype(str)
    .str.strip()
)

df["failure_type"] = (
    df["failure_type"]
    .fillna("")
    .astype(str)
    .str.strip()
)

# Remove empty reports
df = df[df["report_text"] != ""]

# Remove empty labels
df = df[df["failure_type"] != ""]

# Remove exact duplicate report + label combinations
df = df.drop_duplicates(
    subset=["report_text", "failure_type"]
)

df = df.reset_index(drop=True)


print("\nDataset after cleaning:")
print(df.shape)


# ============================================================
# SHOW CLASS DISTRIBUTION
# ============================================================

print("\nFailure Type Distribution:")
print(df["failure_type"].value_counts())


# ============================================================
# LABEL ENCODING
# ============================================================

label_encoder = LabelEncoder()

df["label"] = label_encoder.fit_transform(
    df["failure_type"]
)

num_labels = len(
    label_encoder.classes_
)

print("\nFailure Classes:")

for index, label in enumerate(
    label_encoder.classes_
):

    print(index, "=", label)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

train_df, test_df = train_test_split(
    df,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=df["label"]
)

train_df = train_df.reset_index(drop=True)
test_df = test_df.reset_index(drop=True)


print("\nTraining samples:", len(train_df))
print("Testing samples:", len(test_df))


# ============================================================
# LOAD TOKENIZER
# ============================================================

print("\nLoading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

print("Tokenizer loaded.")


# ============================================================
# TOKENIZATION FUNCTION
# ============================================================

def tokenize_function(examples):

    return tokenizer(
        examples["report_text"],
        padding="max_length",
        truncation=True,
        max_length=MAX_LENGTH
    )


# ============================================================
# CREATE HUGGING FACE DATASETS
# ============================================================

from datasets import Dataset


train_dataset = Dataset.from_pandas(
    train_df[
        ["report_text", "label"]
    ]
)

test_dataset = Dataset.from_pandas(
    test_df[
        ["report_text", "label"]
    ]
)


# ============================================================
# TOKENIZE DATA
# ============================================================

print("\nTokenizing training data...")

train_dataset = train_dataset.map(
    tokenize_function,
    batched=True
)

print("Tokenizing testing data...")

test_dataset = test_dataset.map(
    tokenize_function,
    batched=True
)


# ============================================================
# REMOVE UNNECESSARY COLUMNS
# ============================================================

train_dataset = train_dataset.remove_columns(
    ["report_text"]
)

test_dataset = test_dataset.remove_columns(
    ["report_text"]
)


# Rename label correctly for Transformers
train_dataset = train_dataset.rename_column(
    "label",
    "labels"
)

test_dataset = test_dataset.rename_column(
    "label",
    "labels"
)


# ============================================================
# LOAD DISTILBERT MODEL
# ============================================================

print("\nLoading DistilBERT model...")

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=num_labels
)

print("DistilBERT model loaded.")


# ============================================================
# EVALUATION FUNCTION
# ============================================================

def compute_metrics(eval_prediction):

    predictions, labels = eval_prediction

    predictions = np.argmax(
        predictions,
        axis=1
    )

    accuracy = accuracy_score(
        labels,
        predictions
    )

    return {
        "accuracy": accuracy
    }


# ============================================================
# TRAINING ARGUMENTS
# ============================================================

training_args = TrainingArguments(
    output_dir=MODEL_OUTPUT_DIR,

    num_train_epochs=3,

    per_device_train_batch_size=4,

    per_device_eval_batch_size=4,

    learning_rate=2e-5,

    weight_decay=0.01,

    eval_strategy="epoch",

    save_strategy="epoch",

    report_to="none"
)

# ============================================================
# TRAINER
# ============================================================

trainer = Trainer(

    model=model,

    args=training_args,

    train_dataset=train_dataset,

    eval_dataset=test_dataset,

    compute_metrics=compute_metrics
)


# ============================================================
# TRAIN MODEL
# ============================================================

print("\n========================================")
print(" STARTING DEEP LEARNING TRAINING")
print("========================================\n")

trainer.train()


# ============================================================
# EVALUATION
# ============================================================

print("\n========================================")
print(" MODEL EVALUATION")
print("========================================")

evaluation = trainer.evaluate()

print("\nEvaluation results:")

for key, value in evaluation.items():

    print(
        f"{key}: {value}"
    )


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

predictions = trainer.predict(
    test_dataset
)

predicted_labels = np.argmax(
    predictions.predictions,
    axis=1
)

true_labels = predictions.label_ids


print("\nClassification Report:\n")

print(
    classification_report(
        true_labels,
        predicted_labels,
        target_names=label_encoder.classes_,
        zero_division=0
    )
)


# ============================================================
# SAVE MODEL
# ============================================================

print("\nSaving model...")

os.makedirs(
    MODEL_OUTPUT_DIR,
    exist_ok=True
)

trainer.save_model(
    MODEL_OUTPUT_DIR
)

tokenizer.save_pretrained(
    MODEL_OUTPUT_DIR
)


# Save label names
label_file = os.path.join(
    MODEL_OUTPUT_DIR,
    "labels.txt"
)

with open(
    label_file,
    "w",
    encoding="utf-8"
) as file:

    for label in label_encoder.classes_:

        file.write(
            label + "\n"
        )


print("\n========================================")
print(" TRAINING COMPLETED SUCCESSFULLY")
print("========================================")

print(
    "\nModel saved at:"
)

print(
    MODEL_OUTPUT_DIR
)

print(
    "\nLabels saved at:"
)

print(
    label_file
)