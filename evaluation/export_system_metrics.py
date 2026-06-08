import os
import json
from datetime import datetime, timezone


os.makedirs("paper/reproducibility", exist_ok=True)

system_metrics = {
    "detection_agent_performance": {
        "accuracy": 0.98545,
        "precision": 0.9875290023201856,
        "recall": 0.9321105940323022,
        "f1_score": 0.9590198563582594
    },
    "standalone_threat_analysis_performance": {
        "accuracy": 0.7435,
        "macro_f1": 0.7377,
        "weighted_f1": 0.7352
    },
    "end_to_end_framework_performance": {
        "total_events": 500,
        "detected_attacks": 465,
        "detection_rate": 0.93,
        "operational_threat_classification_accuracy": 0.918,
        "average_detection_confidence": 0.8019982722028624,
        "average_attack_confidence": 0.6784342135293807,
        "average_trust_score": 0.7161556,
        "blockchain_ledger_valid": True,
        "processing_time_seconds": 168.9477,
        "average_time_per_event": 0.337895
    },
    "trust_decision_distribution": {
        "human_review": 330,
        "auto_response": 122,
        "missed_detection": 35,
        "escalate": 13
    },
    "generated_at": datetime.now(timezone.utc).isoformat()
}

with open(
    "paper/reproducibility/system_metrics.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(system_metrics, file, indent=4)

print("Saved: paper/reproducibility/system_metrics.json")