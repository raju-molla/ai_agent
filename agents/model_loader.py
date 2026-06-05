import joblib


DETECTION_FEATURES = [
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


def load_detection_agent():
    return joblib.load("models/detection_agent_v1.pkl")


def detect_attack(model, sample_df):
    sample_df = sample_df[DETECTION_FEATURES]

    prediction = model.predict(sample_df)[0]
    probability = model.predict_proba(sample_df)[0]

    return {
        "prediction": "attack" if prediction == 1 else "normal",
        "confidence": float(max(probability))
    }


def load_threat_agents():
    group_model = joblib.load("models/threat_group_model_v2.pkl")
    group_encoder = joblib.load("models/threat_group_encoder_v2.pkl")

    exact_model = joblib.load("models/threat_exact_model_v2.pkl")
    exact_encoder = joblib.load("models/threat_exact_encoder_v2.pkl")

    features = joblib.load("models/threat_analysis_features_v2.pkl")

    return group_model, group_encoder, exact_model, exact_encoder, features


def analyze_threat(group_model, group_encoder, exact_model, exact_encoder, features, sample_df):
    sample_df = sample_df[features]

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