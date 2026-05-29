"""Tests for parser.py"""

import tempfile
from pathlib import Path

from check_noble_version.parser import get_latest_version_from_upgrades


class TestGetLatestVersionFromUpgrades:
    """Tests for get_latest_version_from_upgrades function"""

    def test_get_latest_version_simple(self):
        """Test extracting latest version from simple MDX content"""
        content = """
| Tag | Name |
|-----|------|
| [`v1.0.0`](url) | Version 1 |
| [`v2.0.0`](url) | Version 2 |
| [`v3.0.0`](url) | Version 3 |
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mdx', delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)
            
            result = get_latest_version_from_upgrades(path)
            assert result == "v3.0.0"
            
            path.unlink()

    def test_get_latest_version_unordered(self):
        """Test extracting latest version when versions are not in order"""
        content = """
| Tag | Name |
|-----|------|
| [`v5.0.0`](url) | Version 5 |
| [`v2.0.0`](url) | Version 2 |
| [`v10.0.0`](url) | Version 10 |
| [`v3.0.0`](url) | Version 3 |
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mdx', delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)
            
            result = get_latest_version_from_upgrades(path)
            assert result == "v10.0.0"
            
            path.unlink()

    def test_get_latest_version_with_suffix_returns_none(self):
        """Test that versions with suffixes cause function to return None"""
        content = """
| Tag | Name |
|-----|------|
| [`v1.0.0`](url) | Version 1 |
| [`v2.0.0-rc1`](url) | RC Version |
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mdx', delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)
            
            result = get_latest_version_from_upgrades(path)
            assert result is None
            
            path.unlink()

    def test_get_latest_version_no_versions_returns_none(self):
        """Test that function returns None when no versions are found"""
        content = """
| Tag | Name |
|-----|------|
| Some content without versions |
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mdx', delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)
            
            result = get_latest_version_from_upgrades(path)
            assert result is None
            
            path.unlink()

    def test_get_latest_version_file_not_found_returns_none(self):
        """Test that function returns None when file doesn't exist"""
        non_existent_path = Path("/tmp/non_existent_file_12345.mdx")
        result = get_latest_version_from_upgrades(non_existent_path)
        assert result is None

