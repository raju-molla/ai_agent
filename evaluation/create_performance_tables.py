import os
import pandas as pd


os.makedirs("paper", exist_ok=True)


# =========================
# Table III: Performance Table
# =========================

performance_table = pd.DataFrame([
    ["Detection Accuracy", "98.54%"],
    ["Detection F1-Score", "95.90%"],
    ["Threat Classification Accuracy", "91.80%"],
    ["Detection Rate", "93.00%"],
    ["Average Detection Confidence", "0.802"],
    ["Average Attack Confidence", "0.678"],
    ["Average Trust Score", "0.716"],
    ["Blockchain Integrity Validation", "100%"],
    ["Total Evaluated Events", "500"],
    ["Average Processing Time", "0.338 sec/event"]
], columns=["Metric", "Value"])


# =========================
# Table IV: Capability Comparison
# =========================

capability_table = pd.DataFrame([
    ["Attack Detection", "Yes", "Yes", "Yes"],
    ["Attack Classification", "No", "Yes", "Yes"],
    ["Explainability", "No", "No", "Yes"],
    ["Automated Response", "No", "Limited", "Yes"],
    ["Trust Evaluation", "No", "No", "Yes"],
    ["Blockchain Logging", "No", "No", "Yes"],
    ["Forensic Audit Trail", "No", "No", "Yes"],
    ["Multi-Agent Architecture", "No", "No", "Yes"]
], columns=[
    "Capability",
    "Traditional IDS",
    "ML-Based IDS",
    "Proposed Framework"
])


# =========================
# Save CSV Files
# =========================

performance_table.to_csv(
    "paper/performance_comparison_table.csv",
    index=False
)

capability_table.to_csv(
    "paper/capability_comparison_table.csv",
    index=False
)


# =========================
# Save Markdown Tables
# =========================

with open("paper/performance_tables.md", "w", encoding="utf-8") as file:
    file.write("# Performance and Capability Comparison Tables\n\n")

    file.write("## Table III. End-to-End Framework Performance\n\n")
    file.write(performance_table.to_markdown(index=False))
    file.write("\n\n")

    file.write("## Table IV. Capability Comparison\n\n")
    file.write(capability_table.to_markdown(index=False))
    file.write("\n")


print("Saved:")
print("paper/performance_comparison_table.csv")
print("paper/capability_comparison_table.csv")
print("paper/performance_tables.md")