"""Tracker file operations."""

import json
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime, timezone

from check_noble_version.config import TRACKER_JSON_PATH


def load_tracker(tracker_path: Optional[Path] = None) -> dict:
    """
    Load the version tracker JSON file.
    
    Args:
        tracker_path: Optional path to tracker file. Defaults to TRACKER_JSON_PATH.
    
    Returns:
        Dictionary with tracker data, or default structure if file doesn't exist
    """
    if tracker_path is None:
        tracker_path = TRACKER_JSON_PATH
    
    if not tracker_path.exists():
        return {
            "last_tracked_version": None,
            "last_checked": None
        }
    
    try:
        with open(tracker_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in tracker file: {e}", file=sys.stderr)
        return {
            "last_tracked_version": None,
            "last_checked": None
        }
    except Exception as e:
        print(f"Error reading tracker file: {e}", file=sys.stderr)
        return {
            "last_tracked_version": None,
            "last_checked": None
        }


def save_tracker(version: str, tracker_path: Optional[Path] = None):
    """
    Save the current version to the tracker JSON file.
    
    Args:
        version: Version string to save
        tracker_path: Optional path to tracker file. Defaults to TRACKER_JSON_PATH.
    """
    if tracker_path is None:
        tracker_path = TRACKER_JSON_PATH
    
    tracker_data = {
        "last_tracked_version": version,
        "last_checked": datetime.now(timezone.utc).isoformat()
    }
    
    try:
        with open(tracker_path, 'w', encoding='utf-8') as f:
            json.dump(tracker_data, f, indent=2)
    except Exception as e:
        print(f"Error writing tracker file: {e}", file=sys.stderr)

