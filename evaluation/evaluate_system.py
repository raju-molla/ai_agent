import time
import pandas as pd

from agents.model_loader import (
    load_detection_agent,
    detect_attack,
    load_threat_agents,
    analyze_threat
)

from agents.response_agent import recommend_response
from agents.trust_manager import calculate_trust_score
from blockchain.blockchain_logger import log_incident, verify_ledger


def main():
    df = pd.read_csv("data/iot_cloud_sec.csv")

    detection_model = load_detection_agent()
    group_model, group_encoder, exact_model, exact_encoder, threat_features = load_threat_agents()

    attack_samples = df[df["label_binary"] == 1].head(500)

    results = []

    start_time = time.time()

    for _, row in attack_samples.iterrows():
        sample = row.to_frame().T

        event_id = sample["event_id"].values[0]
        actual_label = sample["label_multiclass"].values[0]

        detection_result = detect_attack(detection_model, sample)

        if detection_result["prediction"] == "attack":
            threat_result = analyze_threat(
                group_model,
                group_encoder,
                exact_model,
                exact_encoder,
                threat_features,
                sample
            )

            response_result = recommend_response(threat_result)

            trust_result = calculate_trust_score(
                detection_result,
                threat_result
            )

            final_report = {
                "event_id": event_id,
                "actual_label": actual_label,
                "detection": detection_result,
                "threat_analysis": threat_result,
                "response": response_result,
                "trust": trust_result
            }

            log_incident(final_report)

            results.append({
                "event_id": event_id,
                "actual_label": actual_label,
                "detected": 1,
                "predicted_attack_type": threat_result["attack_type"],
                "correct_attack_type": int(threat_result["attack_type"] == actual_label),
                "detection_confidence": detection_result["confidence"],
                "attack_confidence": threat_result["attack_confidence"],
                "trust_score": trust_result["trust_score"],
                "trust_decision": trust_result["decision"]
            })

        else:
            results.append({
                "event_id": event_id,
                "actual_label": actual_label,
                "detected": 0,
                "predicted_attack_type": None,
                "correct_attack_type": 0,
                "detection_confidence": detection_result["confidence"],
                "attack_confidence": 0,
                "trust_score": 0,
                "trust_decision": "missed_detection"
            })

    end_time = time.time()

    results_df = pd.DataFrame(results)

    print("\n=== System Evaluation Summary ===")
    print("Total Events:", len(results_df))
    print("Detected Attacks:", results_df["detected"].sum())
    print("Detection Rate:", results_df["detected"].mean())
    print("Threat Classification Accuracy:", results_df["correct_attack_type"].mean())
    print("Average Detection Confidence:", results_df["detection_confidence"].mean())
    print("Average Attack Confidence:", results_df["attack_confidence"].mean())
    print("Average Trust Score:", results_df["trust_score"].mean())

    print("\nTrust Decision Distribution:")
    print(results_df["trust_decision"].value_counts())

    print("\nBlockchain Ledger Valid:", verify_ledger())

    print("\nProcessing Time Seconds:", round(end_time - start_time, 4))
    print("Average Time Per Event:", round((end_time - start_time) / len(results_df), 6))

    results_df.to_csv("evaluation/system_evaluation_results.csv", index=False)

    print("\nResults saved to: evaluation/system_evaluation_results.csv")


if __name__ == "__main__":
    main()