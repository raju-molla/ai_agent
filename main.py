import pandas as pd

from agents.model_loader import (
    load_detection_agent,
    detect_attack,
    load_threat_agents,
    analyze_threat
)

from agents.response_agent import recommend_response
from agents.trust_manager import calculate_trust_score
from agents.explainability_agent import explain_prediction

from blockchain.blockchain_logger import (
    log_incident,
    verify_ledger
)


def main():

    # =========================
    # Load Dataset
    # =========================

    df = pd.read_csv("data/iot_cloud_sec.csv")

    # =========================
    # Load Models
    # =========================

    detection_model = load_detection_agent()

    (
        group_model,
        group_encoder,
        exact_model,
        exact_encoder,
        threat_features
    ) = load_threat_agents()

    # =========================
    # Select Sample Attack
    # =========================

    sample = df[df["label_binary"] == 1].iloc[[0]]

    event_id = sample["event_id"].values[0]
    actual_label = sample["label_multiclass"].values[0]

    print("\n=== Input Event ===")
    print("Event ID:", event_id)
    print("Actual Label:", actual_label)

    # =========================
    # Detection Agent
    # =========================

    detection_result = detect_attack(
        detection_model,
        sample
    )

    print("\n=== Detection Agent Result ===")
    print(detection_result)

    if detection_result["prediction"] != "attack":
        print("\nNo threat detected.")
        return

    # =========================
    # Threat Analysis Agent
    # =========================

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

    # =========================
    # Explainability Agent
    # =========================

    explanation_result = explain_prediction(
        sample_df=sample,
        feature_names=threat_features,
        feature_importances=exact_model.feature_importances_,
        attack_type=threat_result["attack_type"]
    )

    print("\n=== Explainability Agent Result ===")
    print(explanation_result)

    # =========================
    # Response Agent
    # =========================

    response_result = recommend_response(
        threat_result
    )

    print("\n=== Response Agent Result ===")
    print(response_result)

    # =========================
    # Trust Manager
    # =========================

    trust_result = calculate_trust_score(
        detection_result,
        threat_result
    )

    print("\n=== Trust Manager Result ===")
    print(trust_result)

    # =========================
    # Final Incident Report
    # =========================

    final_report = {
        "event_id": event_id,
        "actual_label": actual_label,
        "detection": detection_result,
        "threat_analysis": threat_result,
        "explanation": explanation_result,
        "response": response_result,
        "trust": trust_result
    }

    print("\n=== Final Incident Report ===")
    print(final_report)

    # =========================
    # Blockchain Logger
    # =========================

    block = log_incident(
        final_report
    )

    print("\n=== Blockchain Logger Result ===")
    print("Block Index:", block["block_index"])
    print("Timestamp:", block["timestamp"])
    print("Previous Hash:", block["previous_hash"])
    print("Block Hash:", block["block_hash"])
    print("Ledger Valid:", verify_ledger())


if __name__ == "__main__":
    main()