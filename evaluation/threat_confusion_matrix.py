import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay


DATA_PATH = "data/iot_cloud_sec.csv"

MODEL_PATH = "models/threat_analysis_agent_v1.pkl"
ENCODER_PATH = "models/threat_label_encoder_v1.pkl"
FEATURES_PATH = "models/threat_analysis_features_v1.pkl"

OUTPUT_DIR = "paper/figures"
TABLE_DIR = "paper/tables"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TABLE_DIR, exist_ok=True)


def main():
    df = pd.read_csv(DATA_PATH)

    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"])
    df = df.sort_values("timestamp_utc").reset_index(drop=True)

    attack_df = df[df["label_binary"] == 1].copy()

    model = joblib.load(MODEL_PATH)
    label_encoder = joblib.load(ENCODER_PATH)
    features = joblib.load(FEATURES_PATH)

    attack_df = attack_df.dropna(subset=["label_multiclass"])

    X = attack_df[features]
    y_text = attack_df["label_multiclass"]
    y = label_encoder.transform(y_text)

    split_index = int(len(attack_df) * 0.8)

    X_test = X.iloc[split_index:]
    y_test = y[split_index:]

    predictions = model.predict(X_test)

    labels = label_encoder.classes_

    cm = confusion_matrix(y_test, predictions)

    report = classification_report(
        y_test,
        predictions,
        target_names=labels,
        output_dict=True,
        zero_division=0
    )

    report_df = pd.DataFrame(report).transpose()

    report_df.to_csv(
        os.path.join(TABLE_DIR, "threat_classification_report.csv")
    )

    plt.figure(figsize=(10, 8))

    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=labels
    )

    display.plot(
        cmap="Blues",
        xticks_rotation=45,
        values_format="d"
    )

    plt.title("Threat Analysis Agent Confusion Matrix")
    plt.tight_layout()

    output_path = os.path.join(
        OUTPUT_DIR,
        "threat_confusion_matrix.png"
    )

    plt.savefig(output_path, dpi=300)
    plt.close()

    print("Saved figure:", output_path)
    print("Saved table:", os.path.join(TABLE_DIR, "threat_classification_report.csv"))

    print("\nClassification Report:")
    print(classification_report(
        y_test,
        predictions,
        target_names=labels,
        zero_division=0
    ))


if __name__ == "__main__":
    main()