"""Tests for version.py"""

import pytest

from check_noble_version.version import parse_version, compare_versions


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

