# IV. Experimental Setup

## A. Dataset Description

The proposed framework was evaluated using the IoT-Cloud-Sec dataset [41], a large-scale cybersecurity dataset specifically designed to represent realistic IoT-cloud environments. The dataset contains 100,000 security events collected from heterogeneous IoT devices, cloud services, communication infrastructures, and operational environments.

Each event is represented by 126 attributes describing device behavior, network traffic characteristics, cloud resource utilization, communication quality indicators, authentication activities, and security-related telemetry. The dataset includes both benign and malicious events, enabling the evaluation of binary attack detection and multi-class threat classification tasks.

The attack scenarios represented in the dataset include unauthorized access, credential theft, replay attacks, malware activity, distributed denial-of-service (DDoS) attacks, MQTT flooding attacks, botnet command-and-control communication, data tampering, and jamming attacks. These attack categories were selected to represent a diverse range of threats commonly observed in contemporary IoT-cloud infrastructures.

The dataset contains approximately 81.95% benign events and 18.05% attack events. The distribution of attack categories is summarized in Table I.

### Table I. Attack Distribution in IoT-Cloud-Sec Dataset

| Attack Type         | Number of Events |
| ------------------- | ---------------- |
| Unauthorized Access | 3,045            |
| DDoS                | 3,015            |
| MQTT Flood          | 3,012            |
| Malware             | 2,010            |
| Credential Theft    | 1,983            |
| Data Tampering      | 1,982            |
| Replay Attack       | 1,017            |
| Botnet C2           | 999              |
| Jamming             | 984              |

The diversity of attack categories allows the proposed framework to be evaluated under realistic multi-threat operational conditions.

## B. Experimental Environment

All experiments were conducted using Python and widely adopted machine learning libraries, including Scikit-learn, Pandas, NumPy, and Joblib. The implementation was developed within a modular multi-agent architecture where each security component operates as an independent software agent.

The Detection Agent and Threat Analysis Agent were implemented using Random Forest classifiers due to their strong performance, robustness against noisy cybersecurity data, and interpretability characteristics [19]. Blockchain functionality was implemented using cryptographic hash chaining to provide immutable incident logging and integrity verification.

The complete framework was executed on a Windows-based development environment and evaluated using offline replay analysis of recorded security events.

## C. Data Preparation

Prior to model training, the dataset was sorted chronologically using the event timestamp attribute. This procedure ensured that the evaluation reflected realistic deployment conditions and prevented future information from influencing past predictions.

Features directly associated with ground-truth labels or attack definitions were excluded from the Detection Agent to avoid information leakage. Consequently, the Detection Agent relied exclusively on operational telemetry, network indicators, communication statistics, and device measurements.

For the Threat Analysis Agent, attack-related features were retained because the objective was to classify the exact attack category rather than merely detect the existence of malicious activity.

Categorical attributes were encoded using label encoding techniques where necessary, and missing values were handled according to the preprocessing requirements of the employed machine learning models.

## D. Detection Agent Evaluation

The Detection Agent was evaluated as a binary classification model responsible for distinguishing between normal and malicious events.

To simulate real-world deployment conditions, a temporal train-test split was employed. The earliest 80% of events were used for training, while the most recent 20% were reserved for testing.

The following evaluation metrics were computed:

* Accuracy
* Precision
* Recall
* F1-Score
* Confusion Matrix

This evaluation strategy provides a more realistic assessment than random sampling because the model is required to generalize to future events that were not available during training.

## E. Threat Analysis Agent Evaluation

The Threat Analysis Agent was evaluated exclusively on malicious events identified within the dataset.

A hierarchical two-stage classification strategy was employed. The first stage classified attacks into broader attack groups, while the second stage identified the exact attack category.

The evaluated metrics included:

* Classification Accuracy
* Macro F1-Score
* Weighted F1-Score
* Confusion Matrix

This evaluation enables the assessment of both coarse-grained and fine-grained threat intelligence generation capabilities.

## F. End-to-End System Evaluation

Beyond evaluating individual agents, the complete cyber defense framework was assessed using an end-to-end evaluation process.

A subset of 500 attack events was processed through the entire pipeline, including:

1. Detection Agent
2. Threat Analysis Agent
3. Explainability Agent
4. Response Agent
5. Trust Manager
6. Blockchain Logger

For each event, the framework generated a complete incident report containing attack predictions, explanations, trust assessments, mitigation recommendations, and immutable blockchain records.

The following system-level metrics were collected:

* Detection Rate
* Threat Classification Accuracy
* Average Detection Confidence
* Average Threat Confidence
* Average Trust Score
* Blockchain Integrity Validation
* Processing Time

This evaluation reflects the practical performance of the complete framework rather than isolated machine learning components.

## G. Trust Evaluation Methodology

The Trust Manager evaluates the reliability of AI-generated security decisions using confidence values produced by the Detection Agent and Threat Analysis Agent.

The trust score is computed as:

[
TrustScore = \frac{C_d + C_t}{2}
]

where (C_d) represents detection confidence and (C_t) represents threat classification confidence.

Based on the resulting trust score, incidents are assigned to one of three operational categories:

* Auto Response
* Human Review
* Escalate

This mechanism enables the framework to balance automation and human oversight while minimizing the risks associated with fully autonomous cybersecurity operations.

## H. Blockchain Integrity Validation

To verify the reliability of the Blockchain Logger, every generated block was validated through hash-chain verification.

For each block, the stored previous hash was compared against the actual hash value of the preceding block. Any inconsistency would indicate potential tampering or data corruption.

The blockchain ledger was considered valid only when all blocks satisfied the hash-chain integrity requirements. This procedure ensured that incident evidence remained immutable throughout the evaluation process.

The experimental design therefore enables comprehensive assessment of detection performance, threat intelligence generation, explainability, trust-aware decision making, and blockchain-based forensic accountability within a unified cybersecurity framework.
