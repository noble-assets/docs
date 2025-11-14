"""Configuration constants for the version tracker."""

from pathlib import Path

# Repository root (parent of scripts directory)
REPO_ROOT = Path(__file__).parent.parent.parent

# Path to mainnet upgrades documentation
MAINNET_MDX_PATH = REPO_ROOT / "docs" / "build" / "chain-upgrades" / "mainnet.mdx"

# Path to version tracker JSON file
TRACKER_JSON_PATH = REPO_ROOT / ".noble_version_tracker.json"

# GitHub repository
GITHUB_REPO = "noble-assets/noble"

