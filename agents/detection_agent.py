import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score


# =========================
# 1. Load Dataset
# =========================

DATA_PATH = "data/iot_cloud_sec.csv"

df = pd.read_csv(DATA_PATH)

df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"])
df = df.sort_values("timestamp_utc").reset_index(drop=True)


# =========================
# 2. Safe Feature Selection
# =========================

safe_features = [
    "install_age_days",
    "device_uptime_s",
    "gateway_uptime_s",
    "maintenance_due_days",
    "firmware_age_days",

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

    "battery_pct",
    "battery_voltage_v",
    "battery_temperature_c",

    "signal_rssi_dbm",
    "signal_snr_db",
    "link_quality_pct",

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
    "cloud_ack_delay_ms"
]

safe_features = [col for col in safe_features if col in df.columns]

X = df[safe_features]
y = df["label_binary"]


# =========================
# 3. Temporal Train/Test Split
# =========================

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


# =========================
# 4. Train Detection Agent
# =========================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    max_depth=5,
    min_samples_leaf=20,
    n_jobs=-1
)

model.fit(X_train, y_train)


# =========================
# 5. Evaluate
# =========================

predictions = model.predict(X_test)

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("\nSummary Metrics:")
print("Accuracy :", accuracy_score(y_test, predictions))
print("Precision:", precision_score(y_test, predictions))
print("Recall   :", recall_score(y_test, predictions))
print("F1 Score :", f1_score(y_test, predictions))


# =========================
# 6. Feature Importance
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
# 7. Save Model
# =========================

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/detection_agent_v1.pkl")

print("\nModel saved: models/detection_agent_v1.pkl")


# =========================
# 8. Detection Function
# =========================

def detect_attack(sample_df):
    prediction = model.predict(sample_df)[0]
    probability = model.predict_proba(sample_df)[0]

    result = {
        "prediction": "attack" if prediction == 1 else "normal",
        "confidence": float(max(probability))
    }

    return result


# =========================
# 9. Test One Sample
# =========================

sample = X_test.iloc[[0]]
result = detect_attack(sample)

print("\nSample Detection Result:")
print(result)