def calculate_trust_score(detection_result, threat_result):

    detection_confidence = detection_result["confidence"]
    attack_confidence = threat_result["attack_confidence"]

    trust_score = (
        detection_confidence +
        attack_confidence
    ) / 2

    if trust_score >= 0.85:
        decision = "auto_response"

    elif trust_score >= 0.60:
        decision = "human_review"

    else:
        decision = "escalate"

    return {
        "trust_score": round(trust_score, 4),
        "decision": decision
    }