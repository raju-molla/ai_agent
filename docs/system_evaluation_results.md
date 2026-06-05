# System Evaluation Results

## Evaluation Configuration

* Total evaluated attack events: 500
* Detection Agent: Random Forest
* Threat Analysis Agent: Two-stage Random Forest architecture
* Response Agent: Rule-based automated response engine
* Trust Manager: Confidence-based trust scoring
* Blockchain Logger: Immutable incident ledger

## Performance Results

| Metric                         | Value           |
| ------------------------------ | --------------- |
| Detection Rate                 | 93.0%           |
| Threat Classification Accuracy | 91.8%           |
| Average Detection Confidence   | 0.802           |
| Average Attack Confidence      | 0.678           |
| Average Trust Score            | 0.716           |
| Blockchain Integrity           | Valid           |
| Average Processing Time        | 0.338 sec/event |

## Trust Decision Distribution

* Human Review: 330
* Auto Response: 122
* Escalate: 13
* Missed Detection: 35

## Observations

The proposed multi-agent cybersecurity framework demonstrated strong detection and classification performance on the IoT-Cloud Security Dataset. The trust management module successfully differentiated between high-confidence incidents suitable for automated response and lower-confidence incidents requiring human review. Blockchain-based logging maintained a valid immutable incident ledger throughout evaluation.
