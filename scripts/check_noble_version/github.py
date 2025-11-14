"""GitHub API integration for fetching diffs."""

import sys
from typing import Optional, Dict, Any

import requests


def get_diff_between_tags(repo: str, base_tag: str, head_tag: str) -> Optional[Dict[str, Any]]:
    """
    Get the diff between two tags from GitHub API.
    
    Args:
        repo: Repository in format 'owner/repo'
        base_tag: Base tag (e.g., 'v11.0.0')
        head_tag: Head tag (e.g., 'v12.0.0')
    
    Returns:
        Dictionary with comparison data from GitHub API, or None on error
    """
    url = f"https://api.github.com/repos/{repo}/compare/{base_tag}...{head_tag}"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching diff from GitHub API: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                if 'message' in error_data:
                    print(f"GitHub API error: {error_data['message']}", file=sys.stderr)
            except (ValueError, KeyError):
                pass
        return None


def format_diff_summary(comparison_data: Dict[str, Any]) -> str:
    """
    Format the GitHub comparison data into a readable summary.
    
    Args:
        comparison_data: Dictionary from GitHub compare API
    
    Returns:
        Formatted string summary
    """
    if not comparison_data:
        return "No diff data available."
    
    summary_lines = []
    
    # Basic info
    status = comparison_data.get('status', 'unknown')
    ahead_by = comparison_data.get('ahead_by', 0)
    behind_by = comparison_data.get('behind_by', 0)
    total_commits = comparison_data.get('total_commits', 0)
    
    summary_lines.append(f"Comparison Status: {status}")
    summary_lines.append(f"Commits ahead: {ahead_by}, behind: {behind_by}, total: {total_commits}")
    summary_lines.append("")
    
    # Files changed
    files = comparison_data.get('files', [])
    if files:
        summary_lines.append(f"Files changed: {len(files)}")
        summary_lines.append("")
        
        # Group by status
        added = [f for f in files if f.get('status') == 'added']
        removed = [f for f in files if f.get('status') == 'removed']
        modified = [f for f in files if f.get('status') == 'modified']
        renamed = [f for f in files if f.get('status') == 'renamed']
        
        if added:
            summary_lines.append(f"Added files ({len(added)}):")
            for f in added[:10]:  # Limit to first 10
                summary_lines.append(f"  + {f.get('filename', 'unknown')}")
            if len(added) > 10:
                summary_lines.append(f"  ... and {len(added) - 10} more")
            summary_lines.append("")
        
        if removed:
            summary_lines.append(f"Removed files ({len(removed)}):")
            for f in removed[:10]:
                summary_lines.append(f"  - {f.get('filename', 'unknown')}")
            if len(removed) > 10:
                summary_lines.append(f"  ... and {len(removed) - 10} more")
            summary_lines.append("")
        
        if modified:
            summary_lines.append(f"Modified files ({len(modified)}):")
            for f in modified[:20]:  # Show more modified files
                changes = f.get('changes', 0)
                additions = f.get('additions', 0)
                deletions = f.get('deletions', 0)
                summary_lines.append(f"  ~ {f.get('filename', 'unknown')} (+{additions}, -{deletions}, {changes} total)")
            if len(modified) > 20:
                summary_lines.append(f"  ... and {len(modified) - 20} more")
            summary_lines.append("")
        
        if renamed:
            summary_lines.append(f"Renamed files ({len(renamed)}):")
            for f in renamed[:10]:
                old_name = f.get('previous_filename', 'unknown')
                new_name = f.get('filename', 'unknown')
                summary_lines.append(f"  → {old_name} → {new_name}")
            if len(renamed) > 10:
                summary_lines.append(f"  ... and {len(renamed) - 10} more")
            summary_lines.append("")
        
        # Filter for relevant files (modules, configs, etc.)
        #
        # TODO: double check this is the correct relevant list
        relevant_files = [
            f for f in files
            if any(keyword in f.get('filename', '').lower() for keyword in [
                'module', 'x/', 'proto', 'upgrade', 'migration', 'changelog', 'release'
            ])
        ]
        
        if relevant_files:
            summary_lines.append("Potentially relevant files for documentation:")
            for f in relevant_files[:15]:
                summary_lines.append(f"  • {f.get('filename', 'unknown')}")
            if len(relevant_files) > 15:
                summary_lines.append(f"  ... and {len(relevant_files) - 15} more")
            summary_lines.append("")
    
    # Commits summary
    commits = comparison_data.get('commits', [])
    if commits:
        summary_lines.append(f"Recent commits ({min(5, len(commits))} of {len(commits)}):")
        for commit in commits[:5]:
            message = commit.get('commit', {}).get('message', '').split('\n')[0]
            sha = commit.get('sha', '')[:7]
            author = commit.get('commit', {}).get('author', {}).get('name', 'unknown')
            summary_lines.append(f"  [{sha}] {message} ({author})")
        if len(commits) > 5:
            summary_lines.append(f"  ... and {len(commits) - 5} more commits")
        summary_lines.append("")
    
    # Add comparison URL
    html_url = comparison_data.get('html_url', '')
    if html_url:
        summary_lines.append(f"Full comparison: {html_url}")
    
    return "\n".join(summary_lines)

