import pandas as pd

ablation_results = pd.DataFrame([
    ["Detection Only", True, False, False, False, False],
    ["Detection + Threat", True, True, False, False, False],
    ["+ Explainability", True, True, True, False, False],
    ["+ Trust Manager", True, True, True, True, False],
    ["Full Framework", True, True, True, True, True]
], columns=[
    "Configuration",
    "Detection",
    "Threat Analysis",
    "Explainability",
    "Trust Management",
    "Blockchain Logging"
])

print(ablation_results)

ablation_results.to_csv(
    "paper/ablation_results.csv",
    index=False
)

print("Saved: paper/ablation_results.csv")