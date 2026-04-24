# calibration_bridge.py -- Bridge between MeTTa calibration logger and ChromaDB
# Author: ClarityClaw autonomous cycle 3527, patched cycle 3544
# Purpose: Write calibration events to ChromaDB so soul_calibration_confidence_query
#          in helper.py can read real data instead of returning INSUFFICIENT-DATA.
# Patch 3544: switched from ephemeral Client() to PersistentClient with writable path
#             so events persist across cycles toward 20+ sample threshold.

import chromadb
import time

CALIBRATION_DB_PATH = "/tmp/continuity_of_mind/data/calibration_db"

def _get_client():
    return chromadb.PersistentClient(path=CALIBRATION_DB_PATH)

def log_calibration_event(outcome, timestamp=None, tag="AGREE"):
    """Log a calibration event to ChromaDB soul_calibration collection.
    Args:
        outcome: 'agree' or 'disagree' (layer1/layer2 agreement)
        timestamp: ISO timestamp string, defaults to now
        tag: classification tag, default AGREE
    Returns: event_id string
    """
    if timestamp is None:
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    try:
        client = _get_client()
        collection = client.get_or_create_collection(name="soul_calibration")
        event_id = f"cal_{outcome}_{timestamp}_{int(time.time()*1000)}"
        collection.add(
            ids=[event_id],
            documents=[f"calibration event: {outcome} at {timestamp}"],
            metadatas=[{"tag": tag, "outcome": outcome, "timestamp": timestamp}]
        )
        return event_id
    except Exception as e:
        return f"ERROR: {str(e)}"


def get_calibration_count():
    """Return count of calibration events in ChromaDB."""
    try:
        client = _get_client()
        collection = client.get_or_create_collection(name="soul_calibration")
        results = collection.get(limit=1000)
        return len(results.get("ids", []))
    except Exception:
        return 0
