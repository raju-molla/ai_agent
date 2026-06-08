import os
import sys
import time
import json
import pandas as pd


# =========================
# Fix import path
# =========================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from agents.model_loader import (
    load_detection_agent,
    detect_attack,
    load_threat_agents,
    analyze_threat
)

from agents.response_agent import recommend_response
from agents.trust_manager import calculate_trust_score
from agents.explainability_agent import explain_prediction
from blockchain.blockchain_logger import log_incident, verify_ledger


# =========================
# Paths
# =========================

DATA_PATH = "data/iot_cloud_sec.csv"

OUTPUT_DIR = "paper/reproducibility"
TABLE_DIR = "paper/tables"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TABLE_DIR, exist_ok=True)


# =========================
# Main Evaluation
# =========================

def main():
    start_time = time.time()

    df = pd.read_csv(DATA_PATH)

    attack_df = df[df["label_binary"] == 1].copy()

    evaluation_sample = attack_df.head(500)

    detection_model = load_detection_agent()

    (
        group_model,
        group_encoder,
        exact_model,
        exact_encoder,
        threat_features
    ) = load_threat_agents()

    results = []

    detected_attacks = 0
    correct_threat_predictions = 0

    detection_confidences = []
    attack_confidences = []
    trust_scores = []
    trust_decisions = []

    for _, row in evaluation_sample.iterrows():
        sample = row.to_frame().T

        event_id = row["event_id"]
        actual_label = row["label_multiclass"]

        detection_result = detect_attack(
            detection_model,
            sample
        )

        detection_confidence = detection_result.get("confidence", 0)

        record = {
            "event_id": event_id,
            "actual_label": actual_label,
            "detection_prediction": detection_result["prediction"],
            "detection_confidence": detection_confidence,
            "attack_group": None,
            "group_confidence": None,
            "predicted_attack_type": None,
            "attack_confidence": None,
            "threat_correct": False,
            "response_severity": None,
            "recommended_actions": None,
            "trust_score": None,
            "trust_decision": "missed_detection",
            "ledger_valid_after_logging": None
        }

        if detection_result["prediction"] == "attack":
            detected_attacks += 1
            detection_confidences.append(detection_confidence)

            threat_result = analyze_threat(
                group_model,
                group_encoder,
                exact_model,
                exact_encoder,
                threat_features,
                sample
            )

            predicted_attack_type = threat_result["attack_type"]
            attack_confidence = threat_result["attack_confidence"]

            attack_confidences.append(attack_confidence)

            threat_correct = predicted_attack_type == actual_label

            if threat_correct:
                correct_threat_predictions += 1

            explanation_result = explain_prediction(
                sample_df=sample,
                feature_names=threat_features,
                feature_importances=exact_model.feature_importances_,
                attack_type=predicted_attack_type
            )
            response_result = recommend_response(threat_result)

            trust_result = calculate_trust_score(
                detection_result,
                threat_result
            )

            trust_score = trust_result["trust_score"]
            trust_decision = trust_result["decision"]

            trust_scores.append(trust_score)
            trust_decisions.append(trust_decision)

            final_report = {
                "event_id": event_id,
                "actual_label": actual_label,
                "detection": detection_result,
                "threat_analysis": threat_result,
                "explanation": explanation_result,
                "response": response_result,
                "trust": trust_result
            }

            log_incident(final_report)
            ledger_valid = verify_ledger()

            record.update({
                "attack_group": threat_result["attack_group"],
                "group_confidence": threat_result["group_confidence"],
                "predicted_attack_type": predicted_attack_type,
                "attack_confidence": attack_confidence,
                "threat_correct": threat_correct,
                "response_severity": response_result["severity"],
                "recommended_actions": " | ".join(
                    response_result["recommended_actions"]
                ),
                "trust_score": trust_score,
                "trust_decision": trust_decision,
                "ledger_valid_after_logging": ledger_valid
            })

        results.append(record)

    end_time = time.time()

    total_events = len(evaluation_sample)
    missed_detections = total_events - detected_attacks

    detection_rate = detected_attacks / total_events

    if detected_attacks > 0:
        threat_accuracy = correct_threat_predictions / detected_attacks
    else:
        threat_accuracy = 0

    avg_detection_confidence = (
        sum(detection_confidences) / len(detection_confidences)
        if detection_confidences else 0
    )

    avg_attack_confidence = (
        sum(attack_confidences) / len(attack_confidences)
        if attack_confidences else 0
    )

    avg_trust_score = (
        sum(trust_scores) / len(trust_scores)
        if trust_scores else 0
    )

    processing_time = end_time - start_time
    avg_time_per_event = processing_time / total_events

    results_df = pd.DataFrame(results)

    per_event_csv_path = os.path.join(
        OUTPUT_DIR,
        "end_to_end_event_results.csv"
    )

    results_df.to_csv(
        per_event_csv_path,
        index=False
    )

    summary = {
        "total_events": total_events,
        "detected_attacks": detected_attacks,
        "missed_detections": missed_detections,
        "detection_rate": detection_rate,
        "threat_classification_accuracy_detected_only": threat_accuracy,
        "average_detection_confidence": avg_detection_confidence,
        "average_attack_confidence": avg_attack_confidence,
        "average_trust_score": avg_trust_score,
        "trust_decision_distribution": results_df["trust_decision"]
        .value_counts()
        .to_dict(),
        "blockchain_ledger_valid": verify_ledger(),
        "processing_time_seconds": processing_time,
        "average_time_per_event": avg_time_per_event
    }

    summary_json_path = os.path.join(
        OUTPUT_DIR,
        "end_to_end_summary.json"
    )

    with open(summary_json_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)

    summary_table_path = os.path.join(
        TABLE_DIR,
        "end_to_end_summary.csv"
    )

    pd.DataFrame([summary]).to_csv(
        summary_table_path,
        index=False
    )

    print("\n=== System Evaluation Summary ===")
    print("Total Events:", total_events)
    print("Detected Attacks:", detected_attacks)
    print("Missed Detections:", missed_detections)
    print("Detection Rate:", detection_rate)
    print(
        "Threat Classification Accuracy Detected Only:",
        threat_accuracy
    )
    print("Average Detection Confidence:", avg_detection_confidence)
    print("Average Attack Confidence:", avg_attack_confidence)
    print("Average Trust Score:", avg_trust_score)

    print("\nTrust Decision Distribution:")
    print(results_df["trust_decision"].value_counts())

    print("\nBlockchain Ledger Valid:", verify_ledger())

    print("\nProcessing Time Seconds:", round(processing_time, 4))
    print("Average Time Per Event:", round(avg_time_per_event, 6))

    print("\nSaved per-event results:", per_event_csv_path)
    print("Saved summary JSON:", summary_json_path)
    print("Saved summary table:", summary_table_path)


if __name__ == "__main__":
    main()