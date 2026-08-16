import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from modules.text_preprocessor import clean_text


DATASET = "data/maintenance_reports.csv"


def train_severity_model():

    df = pd.read_csv(DATASET)

    df["clean_text"] = df["report_text"].apply(clean_text)

    X = df["clean_text"]
    y = df["severity"]

    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                max_features=3000,
                ngram_range=(1, 2)
            )
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000
            )
        )
    ])

    model.fit(X, y)

    joblib.dump(
        model,
        "models/severity_classifier.pkl"
    )

    print("Severity model trained successfully.")


def predict_severity(report):

    model = joblib.load(
        "models/severity_classifier.pkl"
    )

    cleaned_report = clean_text(report)

    prediction = model.predict([cleaned_report])[0]

    probability = max(
        model.predict_proba([cleaned_report])[0]
    )

    return prediction, round(probability * 100, 2)


if __name__ == "__main__":

    train_severity_model()

    report = """
    Machine stopped suddenly and bearing temperature
    became extremely high. Emergency shutdown was required.
    """

    severity, confidence = predict_severity(report)

    print("\nSeverity:", severity)
    print("Confidence:", confidence, "%")