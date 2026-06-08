def calculate_trust_score(detection_result, threat_result):
    detection_confidence = detection_result["confidence"]
    attack_confidence = threat_result["attack_confidence"]

    trust_score = round(
        (detection_confidence + attack_confidence) / 2,
        4
    )

    if trust_score >= 0.85:
        decision = "auto_response"
    elif trust_score >= 0.60:
        decision = "human_review"
    else:
        decision = "escalate"

    return {
        "trust_score": trust_score,
        "decision": decision
    }