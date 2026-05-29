"""Version parsing and comparison utilities."""

from typing import Tuple


def parse_version(version_str: str) -> Tuple[int, int, int]:
    """
    Parse a version string (e.g., 'v11.0.0') into a tuple of (major, minor, patch).
    
    Args:
        version_str: Version string in format 'vX.Y.Z' or 'X.Y.Z'
    
    Returns:
        Tuple of (major, minor, patch) integers
    
    Raises:
        ValueError: If version format is invalid or contains suffixes (e.g., -rc1)
    """
    # Check for version suffixes (e.g., -rc1, -beta, -alpha)
    if '-' in version_str:
        raise ValueError(
            f"Version with suffix detected: '{version_str}'\n"
            f"This tool currently does not support version suffixes (e.g., -rc1, -beta, -alpha).\n"
            f"Please use only release versions in the format 'vX.Y.Z' (e.g., 'v11.0.0')."
        )
    
    # Remove 'v' prefix if present
    version_str = version_str.lstrip('v')
    parts = version_str.split('.')
    if len(parts) != 3:
        raise ValueError(
            f"Invalid version format: '{version_str}'\n"
            f"Expected format: 'vX.Y.Z' or 'X.Y.Z' where X, Y, Z are integers."
        )
    
    try:
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError as e:
        raise ValueError(
            f"Invalid version format: '{version_str}'\n"
            f"All version components must be integers. Error: {e}"
        )


def compare_versions(version1: str, version2: str) -> int:
    """
    Compare two version strings.
    
    Returns:
        -1 if version1 < version2
         0 if version1 == version2
         1 if version1 > version2
    
    Raises:
        ValueError: If either version format is invalid or contains suffixes
    """
    try:
        v1 = parse_version(version1)
        v2 = parse_version(version2)
    except ValueError as e:
        # Re-raise with context about which version failed
        raise ValueError(f"Error comparing versions '{version1}' and '{version2}':\n{e}")
    
    if v1 < v2:
        return -1
    elif v1 > v2:
        return 1
    else:
        return 0

