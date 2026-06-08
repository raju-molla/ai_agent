import json
import os


RULES_PATH = os.path.join("config", "response_rules.json")


def load_response_rules():
    with open(RULES_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def recommend_response(threat_analysis):
    attack_group = threat_analysis.get("attack_group")
    attack_type = threat_analysis.get("attack_type")
    confidence = threat_analysis.get("attack_confidence", 0)

    response_rules = load_response_rules()

    response = response_rules.get(
        attack_type,
        {
            "severity": "unknown",
            "recommended_actions": [
                "Alert security administrator",
                "Manual investigation required"
            ]
        }
    )

    return {
        "attack_group": attack_group,
        "attack_type": attack_type,
        "confidence": confidence,
        "severity": response["severity"],
        "recommended_actions": response["recommended_actions"]
    }


if __name__ == "__main__":
    sample_threat = {
        "attack_group": "access_attack",
        "attack_type": "unauthorized_access",
        "attack_confidence": 0.94
    }

    result = recommend_response(sample_threat)

    print("Response Agent Output:")
    print(result)