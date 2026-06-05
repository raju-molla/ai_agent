import pandas as pd


def explain_prediction(
    sample_df,
    feature_names,
    feature_importances,
    attack_type
):
    """
    Generate explanation for attack prediction.
    """

    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": feature_importances
    })

    top_features = (
        importance_df
        .sort_values("importance", ascending=False)
        .head(5)["feature"]
        .tolist()
    )

    explanation = (
        f"The event was classified as '{attack_type}' "
        f"based primarily on the influence of: "
        f"{', '.join(top_features)}."
    )

    return {
        "attack_type": attack_type,
        "top_features": top_features,
        "explanation": explanation
    }


if __name__ == "__main__":

    test_result = explain_prediction(
        sample_df=None,
        feature_names=[
            "credential_risk_score",
            "port_scan_score",
            "payload_entropy",
            "network_latency_ms",
            "packet_loss_pct"
        ],
        feature_importances=[
            0.30,
            0.25,
            0.20,
            0.15,
            0.10
        ],
        attack_type="unauthorized_access"
    )

    print(test_result)