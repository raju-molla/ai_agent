# Multi-Agent AI Cyber Defense Framework with Blockchain-Based Trust Management and Explainable Threat Intelligence

## Overview

This project presents a Multi-Agent AI Cyber Defense Framework for IoT-Cloud environments. The framework combines machine learning, explainable AI, trust-aware decision making, and blockchain-based incident logging to create an autonomous cybersecurity defense system.

The system analyzes IoT-cloud telemetry data, detects cyberattacks, classifies attack types, recommends mitigation actions, explains AI decisions, calculates trust scores, and stores incident evidence in an immutable blockchain ledger.

---

## Research Contributions

This framework provides:

* AI-based attack detection
* Multi-class threat analysis
* Explainable threat intelligence
* Automated incident response
* Trust-aware autonomous decision making
* Blockchain-based immutable incident logging
* Evaluation using the IoT-Cloud-Sec Dataset

---

## System Architecture

```text
IoT-Cloud-Sec Dataset
          │
          ▼
 ┌─────────────────┐
 │ Detection Agent │
 └─────────────────┘
          │
          ▼
 ┌──────────────────────┐
 │ Threat Analysis Agent│
 └──────────────────────┘
          │
          ▼
 ┌──────────────────────┐
 │ Explainability Agent │
 └──────────────────────┘
          │
          ▼
 ┌─────────────────┐
 │ Response Agent  │
 └─────────────────┘
          │
          ▼
 ┌─────────────────┐
 │ Trust Manager   │
 └─────────────────┘
          │
          ▼
 ┌─────────────────┐
 │ Blockchain Log  │
 └─────────────────┘
```

---

## Project Structure

```text
aiAgent/
│
├── agents/
│   ├── detection_agent.py
│   ├── threat_analysis_agent.py
│   ├── threat_analysis_agent_v2.py
│   ├── response_agent.py
│   ├── trust_manager.py
│   ├── explainability_agent.py
│   ├── model_loader.py
│   └── __init__.py
│
├── blockchain/
│   ├── blockchain_logger.py
│   └── __init__.py
│
├── data/
│   └── iot_cloud_sec.csv
│
├── evaluation/
│   ├── evaluate_system.py
│   └── __init__.py
│
├── models/
│
├── docs/
│
├── paper/
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Dataset

Dataset: IoT-Cloud-Sec

Characteristics:

* 100,000 events
* 126 features
* IoT telemetry
* Cloud telemetry
* Security indicators
* Binary attack labels
* Multi-class attack labels

Attack Categories:

* unauthorized_access
* credential_theft
* replay_attack
* malware
* ddos
* mqtt_flood
* botnet_c2
* data_tampering
* jamming

---

## Agent Descriptions

### 1. Detection Agent

Purpose:

Detect whether an event is malicious or benign.

Input:

* IoT telemetry
* Network telemetry
* Device metrics

Output:

```json
{
  "prediction": "attack",
  "confidence": 0.58
}
```

Performance:

* Accuracy: 98.54%
* F1 Score: 95.90%

---

### 2. Threat Analysis Agent

Purpose:

Classify the exact attack type.

Output:

```json
{
  "attack_group": "access_attack",
  "attack_type": "unauthorized_access",
  "attack_confidence": 0.94
}
```

Performance:

* Threat Classification Accuracy: 91.8%

---

### 3. Explainability Agent

Purpose:

Provide human-readable explanations for AI decisions.

Output:

```json
{
  "top_features": [
    "port_scan_score",
    "credential_risk_score",
    "tamper_score"
  ]
}
```

Example Explanation:

"The event was classified as unauthorized_access based primarily on the influence of port_scan_score, credential_risk_score, and tamper_score."

---

### 4. Response Agent

Purpose:

Recommend mitigation actions.

Example:

```json
{
  "severity": "high",
  "recommended_actions": [
    "Revoke suspicious credentials",
    "Force password reset",
    "Enable multi-factor authentication",
    "Review IAM policy changes"
  ]
}
```

---

### 5. Trust Manager

Purpose:

Calculate trustworthiness of AI decisions.

Formula:

```text
Trust Score =
(Detection Confidence + Attack Confidence) / 2
```

Decision Rules:

```text
Trust Score ≥ 0.85
    → auto_response

0.60 ≤ Trust Score < 0.85
    → human_review

Trust Score < 0.60
    → escalate
```

Example:

```json
{
  "trust_score": 0.7579,
  "decision": "human_review"
}
```

---

### 6. Blockchain Logger

Purpose:

Store incident evidence in an immutable ledger.

Features:

* Hash chaining
* Integrity verification
* Tamper-resistant logging

Example:

```json
{
  "block_index": 3,
  "previous_hash": "...",
  "block_hash": "...",
  "ledger_valid": true
}
```

---

## Evaluation Results

Evaluation Configuration:

* 500 attack events
* Full multi-agent pipeline

Results:

| Metric                         | Value           |
| ------------------------------ | --------------- |
| Detection Rate                 | 93.0%           |
| Threat Classification Accuracy | 91.8%           |
| Average Detection Confidence   | 0.802           |
| Average Attack Confidence      | 0.678           |
| Average Trust Score            | 0.716           |
| Blockchain Integrity           | Valid           |
| Average Processing Time        | 0.338 sec/event |

Trust Decision Distribution:

| Decision         | Count |
| ---------------- | ----- |
| Human Review     | 330   |
| Auto Response    | 122   |
| Escalate         | 13    |
| Missed Detection | 35    |

---

## Installation

Create virtual environment:

```bash
python -m venv venv
```

Activate:

Git Bash:

```bash
source venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the System

Train Detection Agent:

```bash
python agents/detection_agent.py
```

Train Threat Analysis Agent:

```bash
python agents/threat_analysis_agent_v2.py
```

Run Complete Pipeline:

```bash
python main.py
```

Evaluate Framework:

```bash
python -m evaluation.evaluate_system
```

---

## Future Work

* Ethereum smart contract integration
* Hyperledger Fabric deployment
* SHAP-based explainable AI
* Large Language Model security agents
* Federated cyber threat intelligence
* Real-time SIEM integration

---

## Citation

If you use this framework in research, please cite:

**pending**
