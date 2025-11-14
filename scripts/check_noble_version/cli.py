"""Command-line interface for the version tracker."""

import sys

from check_noble_version.config import (
    MAINNET_MDX_PATH,
    GITHUB_REPO,
)
from check_noble_version.parser import get_latest_version_from_upgrades
from check_noble_version.tracker import load_tracker, save_tracker
from check_noble_version.version import compare_versions
from check_noble_version.github import get_diff_between_tags, format_diff_summary
from check_noble_version.modules import (
    get_module_versions_for_tag,
    get_module_diffs,
)


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
        try:
            comparison = compare_versions(last_tracked, latest_version)
        except ValueError as e:
            print(f"\n❌ Error: {e}", file=sys.stderr)
            print("\nPlease ensure both versions are in the format 'vX.Y.Z' without suffixes.", file=sys.stderr)
            sys.exit(1)
        
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
            print(f"\n  Generating diff between {last_tracked} and {latest_version}...")
            
            diff_data = get_diff_between_tags(GITHUB_REPO, last_tracked, latest_version)
            if diff_data:
                print("\n" + "=" * 50)
                print("DIFF SUMMARY")
                print("=" * 50)
                print(format_diff_summary(diff_data))
                print("=" * 50)
                
                # Get module-specific information
                print("\n" + "=" * 50)
                print("MODULE VERSIONS & DIFFS")
                print("=" * 50)
                
                # Get module versions for both tags
                print(f"\nFetching module versions for {last_tracked}...")
                base_modules = get_module_versions_for_tag(GITHUB_REPO, last_tracked)
                print(f"Fetching module versions for {latest_version}...")
                head_modules = get_module_versions_for_tag(GITHUB_REPO, latest_version)
                
                if base_modules and head_modules:
                    print("\nModule Version Changes:")
                    all_module_paths = set(base_modules.keys()) | set(head_modules.keys())
                    for module_path in sorted(all_module_paths):
                        base_version = base_modules.get(module_path, "N/A")
                        head_version = head_modules.get(module_path, "N/A")
                        if base_version != head_version:
                            print(f"  {module_path}: {base_version} → {head_version}")
                        elif base_version != "N/A":
                            print(f"  {module_path}: {base_version} (unchanged)")
                
                # Get module-specific diffs
                print(f"\nFetching module-specific diffs...")
                module_diffs = get_module_diffs(GITHUB_REPO, last_tracked, latest_version)
                
                if module_diffs:
                    print("\nModule-Specific Changes:")
                    for module_path, diff_info in sorted(module_diffs.items()):
                        file_count = len(diff_info['files'])
                        additions = diff_info['total_additions']
                        deletions = diff_info['total_deletions']
                        changes = diff_info['total_changes']
                        print(f"\n  {module_path}:")
                        print(f"    Files changed: {file_count}")
                        print(f"    Changes: +{additions}, -{deletions} ({changes} total)")
                        if file_count <= 10:
                            for file_info in diff_info['files']:
                                status = file_info.get('status', 'unknown')
                                filename = file_info.get('filename', 'unknown')
                                print(f"      [{status}] {filename}")
                        else:
                            for file_info in diff_info['files'][:5]:
                                status = file_info.get('status', 'unknown')
                                filename = file_info.get('filename', 'unknown')
                                print(f"      [{status}] {filename}")
                            print(f"      ... and {file_count - 5} more files")
                else:
                    print("\n  No changes detected in tracked modules.")
                
                print("=" * 50)
            else:
                print(f"\n  ⚠ Could not fetch diff from GitHub API.")
                print(f"  You can view the comparison manually at:")
                print(f"  https://github.com/{GITHUB_REPO}/compare/{last_tracked}...{latest_version}")
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

