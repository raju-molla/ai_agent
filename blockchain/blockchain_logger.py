import os
import json
import hashlib
from datetime import datetime, timezone


LEDGER_PATH = "blockchain/incident_ledger.json"


def generate_hash(data):
    json_data = json.dumps(data, sort_keys=True)
    return hashlib.sha256(json_data.encode()).hexdigest()


def load_ledger():
    if not os.path.exists(LEDGER_PATH):
        return []

    if os.path.getsize(LEDGER_PATH) == 0:
        return []

    try:
        with open(LEDGER_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_ledger(ledger):
    os.makedirs("blockchain", exist_ok=True)

    with open(LEDGER_PATH, "w", encoding="utf-8") as file:
        json.dump(ledger, file, indent=4)


def log_incident(incident_report):
    ledger = load_ledger()

    previous_hash = ledger[-1]["block_hash"] if ledger else "GENESIS"

    block = {
        "block_index": len(ledger) + 1,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "incident_report": incident_report,
        "previous_hash": previous_hash
    }

    block["block_hash"] = generate_hash(block)

    ledger.append(block)
    save_ledger(ledger)

    return block


def verify_ledger():
    ledger = load_ledger()

    for i, block in enumerate(ledger):
        current_hash = block["block_hash"]

        block_copy = block.copy()
        del block_copy["block_hash"]

        recalculated_hash = generate_hash(block_copy)

        if current_hash != recalculated_hash:
            return False

        if i > 0:
            if block["previous_hash"] != ledger[i - 1]["block_hash"]:
                return False

    return True


if __name__ == "__main__":
    sample_report = {
        "event_id": "evt-test-001",
        "attack_type": "ddos",
        "severity": "high",
        "recommended_actions": [
            "Enable rate limiting",
            "Block suspicious source traffic"
        ]
    }

    block = log_incident(sample_report)

    print("Incident logged:")
    print(block)

    print("Ledger valid:", verify_ledger())