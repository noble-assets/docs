"""Unit tests for check_noble_version.py"""

import json
import pytest
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from check_noble_version import (
    parse_version,
    compare_versions,
    get_latest_version_from_upgrades,
    load_tracker,
    save_tracker,
)


class TestParseVersion:
    """Tests for parse_version function"""

    def test_parse_version_with_v_prefix(self):
        """Test parsing version with 'v' prefix"""
        assert parse_version("v11.0.0") == (11, 0, 0)
        assert parse_version("v1.2.3") == (1, 2, 3)
        assert parse_version("v10.5.20") == (10, 5, 20)

    def test_parse_version_without_v_prefix(self):
        """Test parsing version without 'v' prefix"""
        assert parse_version("11.0.0") == (11, 0, 0)
        assert parse_version("1.2.3") == (1, 2, 3)

    def test_parse_version_raises_on_suffix(self):
        """Test that parse_version raises ValueError for versions with suffixes"""
        with pytest.raises(ValueError, match="Version with suffix detected"):
            parse_version("v11.0.0-rc1")
        
        with pytest.raises(ValueError, match="Version with suffix detected"):
            parse_version("v11.0.0-beta")
        
        with pytest.raises(ValueError, match="Version with suffix detected"):
            parse_version("v11.0.0-alpha")

    def test_parse_version_raises_on_invalid_format(self):
        """Test that parse_version raises ValueError for invalid formats"""
        with pytest.raises(ValueError, match="Invalid version format"):
            parse_version("11.0")  # Missing patch version
        
        with pytest.raises(ValueError, match="Invalid version format"):
            parse_version("11")  # Only major version
        
        with pytest.raises(ValueError, match="Invalid version format"):
            parse_version("11.0.0.1")  # Too many parts

    def test_parse_version_raises_on_non_integer(self):
        """Test that parse_version raises ValueError for non-integer components"""
        with pytest.raises(ValueError, match="All version components must be integers"):
            parse_version("v11.0.a")
        
        with pytest.raises(ValueError, match="All version components must be integers"):
            parse_version("v11.x.0")


class TestCompareVersions:
    """Tests for compare_versions function"""

    def test_compare_versions_equal(self):
        """Test comparing equal versions"""
        assert compare_versions("v11.0.0", "v11.0.0") == 0
        assert compare_versions("v1.2.3", "v1.2.3") == 0
        assert compare_versions("11.0.0", "v11.0.0") == 0

    def test_compare_versions_less_than(self):
        """Test comparing when first version is less than second"""
        assert compare_versions("v10.0.0", "v11.0.0") == -1
        assert compare_versions("v11.0.0", "v11.1.0") == -1
        assert compare_versions("v11.0.0", "v11.0.1") == -1
        assert compare_versions("v1.0.0", "v2.0.0") == -1

    def test_compare_versions_greater_than(self):
        """Test comparing when first version is greater than second"""
        assert compare_versions("v11.0.0", "v10.0.0") == 1
        assert compare_versions("v11.1.0", "v11.0.0") == 1
        assert compare_versions("v11.0.1", "v11.0.0") == 1
        assert compare_versions("v2.0.0", "v1.0.0") == 1

    def test_compare_versions_with_suffix_raises(self):
        """Test that compare_versions raises ValueError when versions have suffixes"""
        with pytest.raises(ValueError, match="Error comparing versions"):
            compare_versions("v11.0.0-rc1", "v11.0.0")
        
        with pytest.raises(ValueError, match="Error comparing versions"):
            compare_versions("v11.0.0", "v11.0.0-rc1")


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


class TestLoadTracker:
    """Tests for load_tracker function"""

    def test_load_tracker_file_not_exists(self):
        """Test loading tracker when file doesn't exist"""
        non_existent_path = Path("/tmp/non_existent_tracker_12345.json")
        result = load_tracker(non_existent_path)
        assert result == {
            "last_tracked_version": None,
            "last_checked": None
        }

    def test_load_tracker_valid_file(self):
        """Test loading tracker from valid JSON file"""
        tracker_data = {
            "last_tracked_version": "v11.0.0",
            "last_checked": "2024-01-01T00:00:00Z"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(tracker_data, f)
            f.flush()
            path = Path(f.name)
            
            result = load_tracker(path)
            assert result == tracker_data
            
            path.unlink()

    def test_load_tracker_invalid_json(self):
        """Test loading tracker with invalid JSON returns default"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content {")
            f.flush()
            path = Path(f.name)
            
            result = load_tracker(path)
            assert result == {
                "last_tracked_version": None,
                "last_checked": None
            }
            
            path.unlink()


class TestSaveTracker:
    """Tests for save_tracker function"""

    def test_save_tracker_creates_file(self):
        """Test that save_tracker creates a file with correct content"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            path = Path(f.name)
            path.unlink()  # Delete the file so we can test creation
            
            save_tracker("v11.0.0", path)
            
            assert path.exists()
            with open(path, 'r') as f:
                data = json.load(f)
                assert data["last_tracked_version"] == "v11.0.0"
                assert "last_checked" in data
                assert data["last_checked"] is not None
            
            path.unlink()

