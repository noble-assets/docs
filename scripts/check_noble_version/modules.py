"""Module configuration and Go module tracking."""

from typing import Dict, List, Optional
import re
import sys

try:
    import requests
except ImportError:
    print("Error: requests library is required. Install it with: pip install requests", file=sys.stderr)
    sys.exit(1)

from check_noble_version.config import GITHUB_REPO


# Mapping of module names (as they appear in docs) to their Go module paths
# This should match the modules documented in technical_reference/modules
MODULE_MAPPINGS: Dict[str, List[str]] = {
    "dollar": [
        "dollar.noble.xyz",
        "github.com/noble-assets/dollar",
    ],
    "orbiter": [
        "github.com/noble-assets/orbiter",
    ],
    "forwarding": [
        "github.com/noble-assets/forwarding",
    ],
    "swap": [
        "github.com/noble-assets/swap",
    ],
    "cctp": [
        "github.com/circlefin/noble-cctp",
    ],
    "aura": [
        "github.com/noble-assets/aura",
    ],
    "authority": [
        "github.com/noble-assets/authority",
    ],
    "blockibc": [
        "github.com/noble-assets/blockibc",
    ],
    "fiattokenfactory": [
        "github.com/noble-assets/fiattokenfactory",
    ],
    "florin": [
        "github.com/noble-assets/florin",
    ],
    "globalfee": [
        "github.com/noble-assets/globalfee",
    ],
    "halo": [
        "github.com/noble-assets/halo",
    ],
    "wormhole": [
        "github.com/noble-assets/wormhole",
    ],
}


def get_relevant_module_paths() -> List[str]:
    """
    Get a flat list of all relevant Go module paths.
    
    Returns:
        List of Go module paths that should be tracked
    """
    paths = []
    for module_paths in MODULE_MAPPINGS.values():
        paths.extend(module_paths)
    return sorted(set(paths))  # Remove duplicates and sort


def fetch_go_mod(repo: str, tag: str) -> Optional[str]:
    """
    Fetch the go.mod file content from GitHub for a specific tag.
    
    Args:
        repo: Repository in format 'owner/repo'
        tag: Git tag (e.g., 'v11.0.0')
    
    Returns:
        Content of go.mod file as string, or None on error
    """
    url = f"https://raw.githubusercontent.com/{repo}/{tag}/go.mod"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching go.mod from GitHub: {e}", file=sys.stderr)
        return None


def parse_go_mod(go_mod_content: str) -> Dict[str, str]:
    """
    Parse go.mod content and extract module dependencies.
    
    Args:
        go_mod_content: Content of go.mod file
    
    Returns:
        Dictionary mapping module paths to their versions
    """
    modules = {}
    
    # Pattern to match require statements: require module/path v1.2.3
    # Also handles replace directives and indirect dependencies
    require_pattern = r'^\s*(?:require\s+)?([^\s]+)\s+([^\s]+)(?:\s+//.*)?$'
    
    lines = go_mod_content.split('\n')
    in_require_block = False
    
    for line in lines:
        line = line.strip()
        
        # Check if we're entering a require block
        if line == 'require (':
            in_require_block = True
            continue
        elif line == ')':
            in_require_block = False
            continue
        elif line.startswith('require '):
            in_require_block = False
            # Single line require
            match = re.match(require_pattern, line[8:].strip())
            if match:
                module_path, version = match.groups()
                modules[module_path] = version
            continue
        
        # Handle lines within require block or standalone requires
        if in_require_block or line.startswith(('require ', '\t')):
            match = re.match(require_pattern, line)
            if match:
                module_path, version = match.groups()
                modules[module_path] = version
    
    return modules


def parse_replace_directives(go_mod_content: str) -> Dict[str, str]:
    """
    Parse replace directives from go.mod content.
    
    Args:
        go_mod_content: Content of go.mod file
    
    Returns:
        Dictionary mapping original module paths to their replacement paths
        Format: {original_path: replacement_path}
    """
    replaces = {}
    
    # Pattern to match replace directives:
    # replace old/path => new/path v1.2.3
    # replace old/path => ../local/path
    # replace old/path v1.2.3 => new/path v1.2.3
    replace_pattern = r'^\s*replace\s+([^\s]+)(?:\s+[^\s]+)?\s+=>\s+([^\s]+)(?:\s+[^\s]+)?(?:\s+//.*)?$'
    
    lines = go_mod_content.split('\n')
    in_replace_block = False
    
    for line in lines:
        stripped = line.strip()
        
        # Check if we're entering a replace block
        if stripped == 'replace (':
            in_replace_block = True
            continue
        elif stripped == ')':
            in_replace_block = False
            continue
        elif stripped.startswith('replace '):
            in_replace_block = False
            # Single line replace
            match = re.match(replace_pattern, line)
            if match:
                original_path, replacement_path = match.groups()
                replaces[original_path] = replacement_path
            continue
        
        # Handle lines within replace block (indented lines without 'replace' keyword)
        if in_replace_block and stripped:
            # Pattern for lines within replace block (no 'replace' keyword, just indented)
            # Format: old/path => new/path v1.2.3
            block_pattern = r'^\s+([^\s]+)(?:\s+[^\s]+)?\s+=>\s+([^\s]+)(?:\s+[^\s]+)?(?:\s+//.*)?$'
            match = re.match(block_pattern, line)
            if match:
                original_path, replacement_path = match.groups()
                replaces[original_path] = replacement_path
    
    return replaces


def apply_replace_directives(modules: Dict[str, str], replaces: Dict[str, str]) -> Dict[str, str]:
    """
    Apply replace directives to module dictionary.
    
    If a module has a replace directive, use the replacement path instead.
    
    Args:
        modules: Dictionary mapping module paths to versions
        replaces: Dictionary mapping original paths to replacement paths
    
    Returns:
        Dictionary with replaced module paths
    """
    result = {}
    
    for module_path, version in modules.items():
        # Check if this module has a replace directive
        if module_path in replaces:
            # Use the replacement path instead
            replacement_path = replaces[module_path]
            result[replacement_path] = version
        else:
            # Keep original
            result[module_path] = version
    
    return result


def get_relevant_modules_from_go_mod(go_mod_content: str) -> Dict[str, str]:
    """
    Extract only the relevant modules (from MODULE_MAPPINGS) from go.mod content.
    Applies replace directives before filtering and dynamically includes replacement paths.
    
    Args:
        go_mod_content: Content of go.mod file
    
    Returns:
        Dictionary mapping relevant module paths to their versions (after applying replaces)
        Includes both original and replacement paths if replacements exist
    """
    # Parse modules and replace directives
    all_modules = parse_go_mod(go_mod_content)
    replaces = parse_replace_directives(go_mod_content)
    
    # Get base relevant paths (original module paths from MODULE_MAPPINGS)
    relevant_paths = get_relevant_module_paths()
    
    # Build a set of all relevant paths including replacements
    # If a relevant module has a replace directive, include the replacement path too
    all_relevant_paths = set(relevant_paths)
    for original_path, replacement_path in replaces.items():
        if original_path in relevant_paths:
            # This relevant module has a replacement - include the replacement path
            all_relevant_paths.add(replacement_path)
    
    # Apply replace directives to get the actual modules being used
    modules_with_replaces = apply_replace_directives(all_modules, replaces)
    
    # Filter to relevant modules (checking both original and replacement paths)
    relevant_modules = {}
    
    for module_path, version in modules_with_replaces.items():
        # Check if this module path matches any of our relevant paths (original or replacement)
        for relevant_path in all_relevant_paths:
            if module_path == relevant_path or module_path.startswith(relevant_path + '/'):
                relevant_modules[module_path] = version
                break
    
    return relevant_modules


def get_module_versions_for_tag(repo: str, tag: str) -> Optional[Dict[str, str]]:
    """
    Get relevant module versions for a specific tag.
    
    Args:
        repo: Repository in format 'owner/repo'
        tag: Git tag (e.g., 'v11.0.0')
    
    Returns:
        Dictionary mapping module paths to versions, or None on error
    """
    go_mod_content = fetch_go_mod(repo, tag)
    if not go_mod_content:
        return None
    
    return get_relevant_modules_from_go_mod(go_mod_content)


def _build_module_to_dir_mapping(repo: str, tag: str) -> Dict[str, str]:
    """
    Build a mapping from Go module paths to directory paths, including replacement paths.
    
    Args:
        repo: Repository in format 'owner/repo'
        tag: Git tag to fetch go.mod from
    
    Returns:
        Dictionary mapping Go module paths (original and replacement) to directory paths
    """
    # Base mapping: original module paths to directories
    base_mapping = {
        "dollar.noble.xyz": "x/dollar",
        "github.com/noble-assets/dollar": "x/dollar",
        "github.com/noble-assets/orbiter": "x/orbiter",
        "github.com/noble-assets/forwarding": "x/forwarding",
        "github.com/noble-assets/swap": "x/swap",
        "github.com/circlefin/noble-cctp": "x/cctp",
        "github.com/noble-assets/aura": "x/aura",
        "github.com/noble-assets/authority": "x/authority",
        "github.com/noble-assets/blockibc": "x/blockibc",
        "github.com/noble-assets/fiattokenfactory": "x/fiattokenfactory",
        "github.com/noble-assets/florin": "x/florin",
        "github.com/noble-assets/globalfee": "x/globalfee",
        "github.com/noble-assets/halo": "x/halo",
        "github.com/noble-assets/wormhole": "x/wormhole",
    }
    
    # Fetch go.mod to get replace directives
    go_mod_content = fetch_go_mod(repo, tag)
    if go_mod_content:
        replaces = parse_replace_directives(go_mod_content)
        # Add replacement paths that map to the same directories as their originals
        for original_path, replacement_path in replaces.items():
            if original_path in base_mapping:
                # Map the replacement path to the same directory as the original
                base_mapping[replacement_path] = base_mapping[original_path]
    
    return base_mapping


def get_module_diffs(repo: str, base_tag: str, head_tag: str) -> Dict[str, Dict[str, any]]:
    """
    Get diffs for relevant modules between two tags.
    
    Args:
        repo: Repository in format 'owner/repo'
        base_tag: Base tag (e.g., 'v11.0.0')
        head_tag: Head tag (e.g., 'v12.0.0')
    
    Returns:
        Dictionary mapping module paths to their diff information
    """
    from check_noble_version.github import get_diff_between_tags
    
    # Get full diff between tags
    diff_data = get_diff_between_tags(repo, base_tag, head_tag)
    if not diff_data:
        return {}
    
    # Build module-to-directory mapping dynamically, including replacement paths
    # Use head_tag to get the most current replace directives
    module_to_dir = _build_module_to_dir_mapping(repo, head_tag)
    
    # Filter files in the diff that belong to relevant modules
    files = diff_data.get('files', [])
    module_diffs = {}
    
    for file_info in files:
        filename = file_info.get('filename', '')
        
        # Check if this file belongs to any relevant module directory
        for module_path, module_dir in module_to_dir.items():
            if filename.startswith(module_dir + '/'):
                if module_path not in module_diffs:
                    module_diffs[module_path] = {
                        'files': [],
                        'total_additions': 0,
                        'total_deletions': 0,
                        'total_changes': 0,
                    }
                
                module_diffs[module_path]['files'].append(file_info)
                module_diffs[module_path]['total_additions'] += file_info.get('additions', 0)
                module_diffs[module_path]['total_deletions'] += file_info.get('deletions', 0)
                module_diffs[module_path]['total_changes'] += file_info.get('changes', 0)
                break
    
    return module_diffs

