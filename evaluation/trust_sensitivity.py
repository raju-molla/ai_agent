import os
import pandas as pd
import matplotlib.pyplot as plt


INPUT_FILE = "paper/reproducibility/end_to_end_event_results.csv"

OUTPUT_TABLE_DIR = "paper/tables"
OUTPUT_FIGURE_DIR = "paper/figures"

os.makedirs(OUTPUT_TABLE_DIR, exist_ok=True)
os.makedirs(OUTPUT_FIGURE_DIR, exist_ok=True)


def assign_decision(trust_score, auto_threshold, review_threshold):
    if pd.isna(trust_score):
        return "missed_detection"

    if trust_score >= auto_threshold:
        return "auto_response"

    if trust_score >= review_threshold:
        return "human_review"

    return "escalate"


def main():
    df = pd.read_csv(INPUT_FILE)

    auto_thresholds = [0.70, 0.75, 0.80, 0.85, 0.90]
    review_threshold = 0.60

    results = []

    for auto_threshold in auto_thresholds:
        decisions = df["trust_score"].apply(
            lambda score: assign_decision(
                score,
                auto_threshold,
                review_threshold
            )
        )

        counts = decisions.value_counts().to_dict()

        results.append({
            "auto_response_threshold": auto_threshold,
            "review_threshold": review_threshold,
            "auto_response_events": counts.get("auto_response", 0),
            "human_review_events": counts.get("human_review", 0),
            "escalated_events": counts.get("escalate", 0),
            "missed_detections": counts.get("missed_detection", 0)
        })

    results_df = pd.DataFrame(results)

    table_path = os.path.join(
        OUTPUT_TABLE_DIR,
        "trust_sensitivity_analysis.csv"
    )

    results_df.to_csv(table_path, index=False)

    print("\nTrust Sensitivity Analysis:")
    print(results_df)
    print("\nSaved table:", table_path)

    plt.figure(figsize=(8, 5))

    plt.plot(
        results_df["auto_response_threshold"],
        results_df["auto_response_events"],
        marker="o",
        label="Auto Response"
    )

    plt.plot(
        results_df["auto_response_threshold"],
        results_df["human_review_events"],
        marker="o",
        label="Human Review"
    )

    plt.plot(
        results_df["auto_response_threshold"],
        results_df["escalated_events"],
        marker="o",
        label="Escalate"
    )

    plt.plot(
        results_df["auto_response_threshold"],
        results_df["missed_detections"],
        marker="o",
        label="Missed Detection"
    )

    plt.xlabel("Auto-Response Trust Threshold")
    plt.ylabel("Number of Events")
    plt.title("Trust Threshold Sensitivity Analysis")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    figure_path = os.path.join(
        OUTPUT_FIGURE_DIR,
        "trust_sensitivity_analysis.png"
    )

    plt.savefig(figure_path, dpi=300)
    plt.close()

    print("Saved figure:", figure_path)


if __name__ == "__main__":
    main()