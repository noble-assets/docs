"""MDX file parsing utilities."""

import re
import sys
from pathlib import Path
from typing import Optional

from check_noble_version.version import parse_version, compare_versions


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
    
    # Pattern to match version tags in markdown links: [`vX.Y.Z`](url) or [`vX.Y.Z-suffix`](url)
    # This matches patterns like [`v11.0.0`](https://github.com/...) or [`v11.0.0-rc1`](...)
    # We capture versions with optional suffixes to detect and handle them
    version_pattern = r'\[`(v\d+\.\d+\.\d+(?:-[a-zA-Z0-9]+)?)`\]'
    
    # Find all version matches
    versions = re.findall(version_pattern, content)
    
    if not versions:
        print("Warning: No versions found in the upgrades table", file=sys.stderr)
        return None
    
    # Check for versions with suffixes and report them
    versions_with_suffixes = [v for v in versions if '-' in v]
    if versions_with_suffixes:
        print("\n⚠ Warning: Found versions with suffixes in the upgrades table:", file=sys.stderr)
        for v in versions_with_suffixes:
            print(f"  - {v}", file=sys.stderr)
        print("\nThis tool cannot handle version suffixes (e.g., -rc1, -beta, -alpha).", file=sys.stderr)
        print("Please update the documentation to use only release versions.", file=sys.stderr)
        print("\nError details:", file=sys.stderr)
        try:
            # Try to parse one to trigger the error message
            parse_version(versions_with_suffixes[0])
        except ValueError as e:
            print(f"{e}", file=sys.stderr)
        return None
    
    # Find the latest version by comparing all found versions
    try:
        latest_version = versions[0]
        for version in versions[1:]:
            if compare_versions(version, latest_version) > 0:
                latest_version = version
    except ValueError as e:
        print(f"\nError: Failed to compare versions: {e}", file=sys.stderr)
        return None
    
    return latest_version

