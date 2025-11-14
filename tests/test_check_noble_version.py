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
    get_diff_between_tags,
    format_diff_summary,
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


class TestGetDiffBetweenTags:
    """Tests for get_diff_between_tags function"""

    def test_get_diff_between_tags_invalid_repo(self):
        """Test that function returns None for invalid repository"""
        result = get_diff_between_tags("invalid/repo", "v1.0.0", "v2.0.0")
        assert result is None

    def test_get_diff_between_tags_invalid_tags(self):
        """Test that function returns None for invalid tags"""
        result = get_diff_between_tags("noble-assets/noble", "v999.999.999", "v999.999.998")
        assert result is None


class TestFormatDiffSummary:
    """Tests for format_diff_summary function"""

    def test_format_diff_summary_empty(self):
        """Test formatting empty diff data"""
        result = format_diff_summary({})
        assert "No diff data available" in result

    def test_format_diff_summary_basic(self):
        """Test formatting basic diff data"""
        comparison_data = {
            "status": "ahead",
            "ahead_by": 5,
            "behind_by": 0,
            "total_commits": 5,
            "files": [
                {"filename": "x/module/file.go", "status": "modified", "additions": 10, "deletions": 5, "changes": 15},
                {"filename": "test.go", "status": "added", "additions": 20, "deletions": 0, "changes": 20},
            ],
            "commits": [
                {
                    "sha": "abc1234",
                    "commit": {
                        "message": "Add new feature",
                        "author": {"name": "Test Author"}
                    }
                }
            ],
            "html_url": "https://github.com/noble-assets/noble/compare/v1...v2"
        }
        result = format_diff_summary(comparison_data)
        assert "Comparison Status: ahead" in result
        assert "Commits ahead: 5" in result
        assert "Files changed: 2" in result
        assert "x/module/file.go" in result
        assert "Add new feature" in result
        assert "https://github.com/noble-assets/noble/compare/v1...v2" in result

    def test_format_diff_summary_relevant_files(self):
        """Test that relevant files are highlighted"""
        comparison_data = {
            "status": "ahead",
            "ahead_by": 1,
            "behind_by": 0,
            "total_commits": 1,
            "files": [
                {"filename": "x/module/file.go", "status": "modified", "additions": 10, "deletions": 5, "changes": 15},
                {"filename": "proto/upgrade.proto", "status": "modified", "additions": 5, "deletions": 2, "changes": 7},
                {"filename": "unrelated.go", "status": "modified", "additions": 1, "deletions": 1, "changes": 2},
            ],
            "commits": [],
            "html_url": ""
        }
        result = format_diff_summary(comparison_data)
        assert "Potentially relevant files for documentation:" in result
        assert "x/module/file.go" in result
        assert "proto/upgrade.proto" in result

