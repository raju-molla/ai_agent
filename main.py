import pandas as pd

from agents.model_loader import (
    load_detection_agent,
    detect_attack,
    load_threat_agents,
    analyze_threat
)

from agents.response_agent import recommend_response
from blockchain.blockchain_logger import log_incident, verify_ledger


def main():
    df = pd.read_csv("data/iot_cloud_sec.csv")

    detection_model = load_detection_agent()

    group_model, group_encoder, exact_model, exact_encoder, threat_features = load_threat_agents()

    sample = df[df["label_binary"] == 1].iloc[[0]]

    event_id = sample["event_id"].values[0]
    actual_label = sample["label_multiclass"].values[0]

    print("\n=== Input Event ===")
    print("Event ID:", event_id)
    print("Actual Label:", actual_label)

    detection_result = detect_attack(detection_model, sample)

    print("\n=== Detection Agent Result ===")
    print(detection_result)

    if detection_result["prediction"] == "attack":
        threat_result = analyze_threat(
            group_model,
            group_encoder,
            exact_model,
            exact_encoder,
            threat_features,
            sample
        )

        print("\n=== Threat Analysis Agent Result ===")
        print(threat_result)

        response_result = recommend_response(threat_result)

        print("\n=== Response Agent Result ===")
        print(response_result)

        final_report = {
            "event_id": event_id,
            "actual_label": actual_label,
            "detection": detection_result,
            "threat_analysis": threat_result,
            "response": response_result
        }

        print("\n=== Final Incident Report ===")
        print(final_report)

        block = log_incident(final_report)

        print("\n=== Blockchain Logger Result ===")
        print("Block Index:", block["block_index"])
        print("Timestamp:", block["timestamp"])
        print("Previous Hash:", block["previous_hash"])
        print("Block Hash:", block["block_hash"])
        print("Ledger Valid:", verify_ledger())

    else:
        print("\nNo threat detected. No response required.")


if __name__ == "__main__":
    main()