#!/usr/bin/env python3
"""
Noble Documentation Version Tracker

This script checks the latest Noble version from the chain upgrades documentation
and compares it with the last tracked version. If there's a mismatch, it can
generate a diff and suggest documentation updates.
"""

import json
import re
import sys
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime, timezone


# Configuration
REPO_ROOT = Path(__file__).parent.parent
MAINNET_MDX_PATH = REPO_ROOT / "docs" / "build" / "chain-upgrades" / "mainnet.mdx"
TRACKER_JSON_PATH = REPO_ROOT / ".noble_version_tracker.json"
GITHUB_REPO = "noble-assets/noble"


def parse_version(version_str: str) -> Tuple[int, int, int]:
    """
    Parse a version string (e.g., 'v11.0.0') into a tuple of (major, minor, patch).
    
    Args:
        version_str: Version string in format 'vX.Y.Z' or 'X.Y.Z'
    
    Returns:
        Tuple of (major, minor, patch) integers
    """
    # Remove 'v' prefix if present
    version_str = version_str.lstrip('v')
    parts = version_str.split('.')
    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {version_str}")
    return (int(parts[0]), int(parts[1]), int(parts[2]))


def compare_versions(version1: str, version2: str) -> int:
    """
    Compare two version strings.
    
    Returns:
        -1 if version1 < version2
         0 if version1 == version2
         1 if version1 > version2
    """
    v1 = parse_version(version1)
    v2 = parse_version(version2)
    
    if v1 < v2:
        return -1
    elif v1 > v2:
        return 1
    else:
        return 0


def get_latest_version_from_upgrades(mdx_path: Path) -> Optional[str]:
    """
    Parse the mainnet.mdx file and extract the latest version from the upgrades table.
    
    Args:
        mdx_path: Path to the mainnet.mdx file
    
    Returns:
        Latest version string (e.g., 'v11.0.0') or None if not found
    """
    try:
        with open(mdx_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {mdx_path}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error reading file {mdx_path}: {e}", file=sys.stderr)
        return None
    
    # Pattern to match version tags in markdown links: [`vX.Y.Z`](url)
    # This matches patterns like [`v11.0.0`](https://github.com/...)
    version_pattern = r'\[`(v\d+\.\d+\.\d+)`\]'
    
    # Find all version matches
    versions = re.findall(version_pattern, content)
    
    if not versions:
        print("Warning: No versions found in the upgrades table", file=sys.stderr)
        return None
    
    # Find the latest version by comparing all found versions
    latest_version = versions[0]
    for version in versions[1:]:
        if compare_versions(version, latest_version) > 0:
            latest_version = version
    
    return latest_version


def load_tracker() -> dict:
    """
    Load the version tracker JSON file.
    
    Returns:
        Dictionary with tracker data, or default structure if file doesn't exist
    """
    if not TRACKER_JSON_PATH.exists():
        return {
            "last_tracked_version": None,
            "last_checked": None
        }
    
    try:
        with open(TRACKER_JSON_PATH, 'r', encoding='utf-8') as f:
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


def save_tracker(version: str):
    """
    Save the current version to the tracker JSON file.
    
    Args:
        version: Version string to save
    """
    tracker_data = {
        "last_tracked_version": version,
        "last_checked": datetime.now(timezone.utc).isoformat()
    }
    
    try:
        with open(TRACKER_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(tracker_data, f, indent=2)
    except Exception as e:
        print(f"Error writing tracker file: {e}", file=sys.stderr)


def main():
    """Main function to check version and compare with tracker."""
    print("Noble Documentation Version Tracker")
    print("=" * 50)
    
    # Get latest version from upgrades table
    print(f"\nReading upgrades from: {MAINNET_MDX_PATH}")
    latest_version = get_latest_version_from_upgrades(MAINNET_MDX_PATH)
    
    if not latest_version:
        print("Error: Could not determine latest version from upgrades table", file=sys.stderr)
        sys.exit(1)
    
    print(f"Latest version in upgrades table: {latest_version}")
    
    # Load tracker
    tracker = load_tracker()
    last_tracked = tracker.get("last_tracked_version")
    
    if last_tracked:
        print(f"Last tracked version: {last_tracked}")
        
        # Compare versions
        comparison = compare_versions(last_tracked, latest_version)
        
        if comparison == 0:
            print("\n✓ Versions match! Documentation is up to date.")
            # Update last_checked timestamp
            save_tracker(latest_version)
            sys.exit(0)
        elif comparison < 0:
            print(f"\n⚠ Version mismatch detected!")
            print(f"  Last tracked: {last_tracked}")
            print(f"  Latest in docs: {latest_version}")
            print(f"\n  The documentation has been updated with a new version.")
            print(f"  Next step: Generate diff between {last_tracked} and {latest_version}")
            # TODO: Generate diff and LLM suggestions
        else:
            print(f"\n⚠ Warning: Last tracked version ({last_tracked}) is newer than latest in docs ({latest_version})")
            print("  This shouldn't happen - the docs may have been reverted.")
    else:
        print("\nNo previous version tracked (first run)")
        print(f"Setting initial tracked version to: {latest_version}")
        save_tracker(latest_version)
        print("\n✓ Tracker initialized. Run again to check for updates.")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()

