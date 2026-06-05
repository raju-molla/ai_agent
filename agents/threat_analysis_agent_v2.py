import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, f1_score


df = pd.read_csv("data/iot_cloud_sec.csv")
df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"])
df = df.sort_values("timestamp_utc").reset_index(drop=True)

attack_df = df[df["label_binary"] == 1].copy()


def map_attack_group(label):
    if label in ["ddos", "mqtt_flood", "botnet_c2"]:
        return "network_flooding"
    if label in ["unauthorized_access", "credential_theft", "replay_attack"]:
        return "access_attack"
    if label == "data_tampering":
        return "integrity_attack"
    if label == "malware":
        return "malware_attack"
    if label == "jamming":
        return "signal_attack"
    return "unknown"


attack_df["attack_group"] = attack_df["label_multiclass"].apply(map_attack_group)

features = [
    "install_age_days", "device_uptime_s", "gateway_uptime_s",
    "maintenance_due_days", "firmware_age_days",

    "sensor_temperature_c", "sensor_humidity_pct",
    "sensor_pressure_hpa", "sensor_vibration_g",
    "sensor_sound_db", "sensor_light_lux",
    "sensor_co2_ppm", "sensor_pm25_ugm3",
    "sensor_voltage_v", "sensor_current_a",
    "sensor_power_w", "sensor_energy_kwh",

    "battery_pct", "battery_voltage_v", "battery_temperature_c",
    "signal_rssi_dbm", "signal_snr_db", "link_quality_pct",

    "payload_entropy", "uplink_kb", "downlink_kb",
    "network_latency_ms", "jitter_ms", "packet_loss_pct",
    "mqtt_qos", "mqtt_topic_depth", "coap_response_code",
    "http_status_code", "tls_handshake_ms", "dns_lookup_ms",
    "edge_to_cloud_delay_ms", "cloud_ack_delay_ms",

    "port_scan_score", "ddos_score", "malware_score",
    "tamper_score", "credential_risk_score"
]

features = [col for col in features if col in attack_df.columns]

X = attack_df[features]

split_index = int(len(attack_df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]


# =========================
# Stage 1: Attack Group Classifier
# =========================

group_encoder = LabelEncoder()

y_group = group_encoder.fit_transform(attack_df["attack_group"])

y_group_train = y_group[:split_index]
y_group_test = y_group[split_index:]

group_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    max_depth=12,
    min_samples_leaf=5,
    class_weight="balanced",
    n_jobs=-1
)

group_model.fit(X_train, y_group_train)

group_predictions = group_model.predict(X_test)

print("\n===== Stage 1: Attack Group Classification =====")
print(
    classification_report(
        y_group_test,
        group_predictions,
        target_names=group_encoder.classes_,
        zero_division=0
    )
)

print("Group Accuracy:", accuracy_score(y_group_test, group_predictions))
print("Group Macro F1:", f1_score(y_group_test, group_predictions, average="macro"))


# =========================
# Stage 2: Exact Attack Classifier
# =========================

exact_encoder = LabelEncoder()

y_exact = exact_encoder.fit_transform(attack_df["label_multiclass"])

y_exact_train = y_exact[:split_index]
y_exact_test = y_exact[split_index:]

exact_model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    max_depth=16,
    min_samples_leaf=3,
    class_weight="balanced",
    n_jobs=-1
)

exact_model.fit(X_train, y_exact_train)

exact_predictions = exact_model.predict(X_test)

print("\n===== Stage 2: Exact Attack Classification =====")
print(
    classification_report(
        y_exact_test,
        exact_predictions,
        target_names=exact_encoder.classes_,
        zero_division=0
    )
)

print("Exact Accuracy:", accuracy_score(y_exact_test, exact_predictions))
print("Exact Macro F1:", f1_score(y_exact_test, exact_predictions, average="macro"))
print("Exact Weighted F1:", f1_score(y_exact_test, exact_predictions, average="weighted"))


# =========================
# Save Models
# =========================

os.makedirs("models", exist_ok=True)

joblib.dump(group_model, "models/threat_group_model_v2.pkl")
joblib.dump(group_encoder, "models/threat_group_encoder_v2.pkl")

joblib.dump(exact_model, "models/threat_exact_model_v2.pkl")
joblib.dump(exact_encoder, "models/threat_exact_encoder_v2.pkl")
joblib.dump(features, "models/threat_analysis_features_v2.pkl")

print("\nSaved Phase 2 v2 models.")


# =========================
# Inference Function
# =========================

def analyze_threat(sample_df):
    group_pred = group_model.predict(sample_df)[0]
    exact_pred = exact_model.predict(sample_df)[0]

    group_prob = group_model.predict_proba(sample_df)[0]
    exact_prob = exact_model.predict_proba(sample_df)[0]

    return {
        "attack_group": group_encoder.inverse_transform([group_pred])[0],
        "group_confidence": float(max(group_prob)),
        "attack_type": exact_encoder.inverse_transform([exact_pred])[0],
        "attack_confidence": float(max(exact_prob))
    }


sample = X_test.iloc[[0]]
print("\nSample Threat Analysis:")
print(analyze_threat(sample))