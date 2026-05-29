"""Tests for tracker.py"""

import json
import tempfile
from pathlib import Path

from check_noble_version.tracker import load_tracker, save_tracker


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

