"""Tests for github.py"""

from check_noble_version.github import get_diff_between_tags, format_diff_summary


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

