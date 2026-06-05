# Trust Manager and Blockchain Evaluation

## Objective

To enhance the Multi-Agent AI Cyber Defense Framework with a trust-aware decision mechanism and immutable blockchain-based incident logging.

## System Workflow

Input Event
→ Detection Agent
→ Threat Analysis Agent
→ Response Agent
→ Trust Manager
→ Blockchain Logger

## Experimental Example

Event ID: evt-000000003

Actual Attack Type: unauthorized_access

### Detection Agent Output

Prediction: Attack

Confidence: 0.5777

### Threat Analysis Agent Output

Attack Group: access_attack

Group Confidence: 0.9977

Attack Type: unauthorized_access

Attack Confidence: 0.9382

### Response Agent Output

Severity: High

Recommended Actions:

* Revoke suspicious credentials
* Force password reset
* Enable multi-factor authentication
* Review IAM policy changes

### Trust Manager Output

Trust Score:

0.7579

Decision:

human_review

### Trust Score Formula

Trust Score = (Detection Confidence + Attack Confidence) / 2

Trust Score = (0.5777 + 0.9382) / 2

Trust Score = 0.7579

### Decision Rules

Trust Score ≥ 0.85 → auto_response

0.60 ≤ Trust Score < 0.85 → human_review

Trust Score < 0.60 → escalate

## Blockchain Logging

Block Index: 3

Ledger Validation: True

Previous Hash:
ac6344b8a0f6fb683b5679aa631c52012382ddd159df4ebfcf069c3cffc049ce

Block Hash:
f3c45e7b1366e6a7bf953105a15ea6dc184a5a2bdecee525dd38434e88b39424

## Conclusion

The proposed framework successfully integrates AI-driven cyber defense agents with a blockchain-based immutable evidence ledger and trust-aware decision mechanism. The Trust Manager provides confidence-based decision support, while the Blockchain Logger ensures tamper-resistant storage of incident evidence and response actions.
