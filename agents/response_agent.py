def recommend_response(threat_analysis):
    attack_group = threat_analysis.get("attack_group")
    attack_type = threat_analysis.get("attack_type")
    confidence = threat_analysis.get("attack_confidence", 0)

    responses = {
        "network_flooding": {
            "severity": "high",
            "actions": [
                "Enable rate limiting",
                "Block suspicious source traffic",
                "Scale gateway resources",
                "Monitor packet loss and latency"
            ]
        },
        "access_attack": {
            "severity": "high",
            "actions": [
                "Revoke suspicious credentials",
                "Force password reset",
                "Enable multi-factor authentication",
                "Review IAM policy changes"
            ]
        },
        "malware_attack": {
            "severity": "critical",
            "actions": [
                "Isolate affected device",
                "Run malware scan",
                "Block command-and-control communication",
                "Collect forensic evidence"
            ]
        },
        "integrity_attack": {
            "severity": "critical",
            "actions": [
                "Freeze affected data pipeline",
                "Validate recent data changes",
                "Restore from trusted backup",
                "Start forensic investigation"
            ]
        },
        "signal_attack": {
            "severity": "medium",
            "actions": [
                "Switch communication channel",
                "Increase signal monitoring",
                "Check gateway interference",
                "Alert network administrator"
            ]
        }
    }

    response = responses.get(
        attack_group,
        {
            "severity": "unknown",
            "actions": ["Alert security administrator"]
        }
    )

    return {
        "attack_group": attack_group,
        "attack_type": attack_type,
        "confidence": confidence,
        "severity": response["severity"],
        "recommended_actions": response["actions"]
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