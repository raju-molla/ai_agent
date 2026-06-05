import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from sklearn.preprocessing import LabelEncoder


# =========================
# 1. Load Dataset
# =========================

DATA_PATH = "data/iot_cloud_sec.csv"

df = pd.read_csv(DATA_PATH)

df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"])
df = df.sort_values("timestamp_utc").reset_index(drop=True)


# =========================
# 2. Use Attack Records Only
# =========================

attack_df = df[df["label_binary"] == 1].copy()

print("Attack records:", attack_df.shape[0])
print("\nAttack class distribution:")
print(attack_df["label_multiclass"].value_counts())


# =========================
# 3. Controlled Feature Selection
# =========================

features = [
    # IoT/device lifecycle
    "install_age_days",
    "device_uptime_s",
    "gateway_uptime_s",
    "maintenance_due_days",
    "firmware_age_days",

    # Sensor telemetry
    "sensor_temperature_c",
    "sensor_humidity_pct",
    "sensor_pressure_hpa",
    "sensor_vibration_g",
    "sensor_sound_db",
    "sensor_light_lux",
    "sensor_co2_ppm",
    "sensor_pm25_ugm3",
    "sensor_voltage_v",
    "sensor_current_a",
    "sensor_power_w",
    "sensor_energy_kwh",

    # Battery and signal
    "battery_pct",
    "battery_voltage_v",
    "battery_temperature_c",
    "signal_rssi_dbm",
    "signal_snr_db",
    "link_quality_pct",

    # Network behaviour
    "payload_entropy",
    "uplink_kb",
    "downlink_kb",
    "network_latency_ms",
    "jitter_ms",
    "packet_loss_pct",
    "mqtt_qos",
    "mqtt_topic_depth",
    "coap_response_code",
    "http_status_code",
    "tls_handshake_ms",
    "dns_lookup_ms",
    "edge_to_cloud_delay_ms",
    "cloud_ack_delay_ms",

    # Controlled security-risk indicators
    # These are not direct labels, but they help distinguish attack families.
    "port_scan_score",
    "ddos_score",
    "malware_score",
    "tamper_score",
    "credential_risk_score"
]

features = [col for col in features if col in attack_df.columns]

X = attack_df[features]
y = attack_df["label_multiclass"]


# =========================
# 4. Encode Labels
# =========================

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

print("\nEncoded classes:")
for index, class_name in enumerate(label_encoder.classes_):
    print(index, "=", class_name)


# =========================
# 5. Temporal Split
# =========================

split_index = int(len(attack_df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y_encoded[:split_index]
y_test = y_encoded[split_index:]


# =========================
# 6. Train Threat Analysis Agent
# =========================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    max_depth=12,
    min_samples_leaf=5,
    class_weight="balanced",
    n_jobs=-1
)

model.fit(X_train, y_train)


# =========================
# 7. Evaluate Model
# =========================

predictions = model.predict(X_test)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        target_names=label_encoder.classes_,
        zero_division=0
    )
)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("\nSummary Metrics:")
print("Accuracy   :", accuracy_score(y_test, predictions))
print("Macro F1   :", f1_score(y_test, predictions, average="macro"))
print("Weighted F1:", f1_score(y_test, predictions, average="weighted"))


# =========================
# 8. Feature Importance
# =========================

importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
})

print("\nTop 20 Features:")
print(
    importance
    .sort_values("importance", ascending=False)
    .head(20)
)


# =========================
# 9. Save Model and Encoder
# =========================

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/threat_analysis_agent_v1.pkl")
joblib.dump(label_encoder, "models/threat_label_encoder_v1.pkl")
joblib.dump(features, "models/threat_analysis_features_v1.pkl")

print("\nModel saved: models/threat_analysis_agent_v1.pkl")
print("Label encoder saved: models/threat_label_encoder_v1.pkl")
print("Feature list saved: models/threat_analysis_features_v1.pkl")


# =========================
# 10. Threat Analysis Function
# =========================

def analyze_threat(sample_df):
    prediction = model.predict(sample_df)[0]
    probabilities = model.predict_proba(sample_df)[0]

    attack_type = label_encoder.inverse_transform([prediction])[0]
    confidence = float(max(probabilities))

    result = {
        "attack_type": attack_type,
        "confidence": confidence
    }

    return result


# =========================
# 11. Test One Sample
# =========================

sample = X_test.iloc[[0]]
result = analyze_threat(sample)

print("\nSample Threat Analysis Result:")
print(result)