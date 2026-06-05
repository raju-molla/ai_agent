# Phase 1: Detection Agent Results

## Objective

Develop an AI-based Detection Agent capable of identifying cyber attacks in IoT-Cloud environments.

## Dataset

IoT-Cloud-Sec Dataset

## Model

Random Forest Classifier

## Experimental Setup

* Safe feature selection
* Temporal train/test split (80/20)
* Leakage-prone security indicators removed
* Evaluation performed on unseen future records

## Results

Accuracy: 98.54%

Precision: 98.75%

Recall: 93.21%

F1-Score: 95.90%

Confusion Matrix:

[[16304, 43],
[248, 3405]]

## Key Features

1. jitter_ms
2. network_latency_ms
3. uplink_kb
4. edge_to_cloud_delay_ms
5. packet_loss_pct

## Conclusion

The Detection Agent achieved 98.54% accuracy and 95.90% F1-score using safe IoT/network telemetry features under temporal split evaluation. The model successfully distinguishes normal and malicious activities without relying on direct attack labels or security-event leakage features.
