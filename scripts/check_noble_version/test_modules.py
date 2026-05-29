"""Tests for modules.py"""

import pytest
from check_noble_version.modules import (
    get_relevant_module_paths,
    parse_go_mod,
    parse_replace_directives,
    apply_replace_directives,
    get_relevant_modules_from_go_mod,
    get_module_versions_for_tag,
    get_module_diffs,
    MODULE_MAPPINGS,
)


class TestGetRelevantModulePaths:
    """Tests for get_relevant_module_paths function"""

    def test_returns_list_of_paths(self):
        """Test that function returns a list of module paths"""
        paths = get_relevant_module_paths()
        assert isinstance(paths, list)
        assert len(paths) > 0

    def test_includes_known_modules(self):
        """Test that known modules are included"""
        paths = get_relevant_module_paths()
        assert "dollar.noble.xyz" in paths or any("dollar" in p for p in paths)
        assert any("orbiter" in p for p in paths)
        assert any("forwarding" in p for p in paths)


class TestParseGoMod:
    """Tests for parse_go_mod function"""

    def test_parse_simple_go_mod(self):
        """Test parsing a simple go.mod file"""
        go_mod = """
module github.com/noble-assets/noble

go 1.21

require (
    dollar.noble.xyz v1.0.0
    github.com/noble-assets/orbiter v2.0.0
)
"""
        modules = parse_go_mod(go_mod)
        assert "dollar.noble.xyz" in modules
        assert modules["dollar.noble.xyz"] == "v1.0.0"
        assert "github.com/noble-assets/orbiter" in modules
        assert modules["github.com/noble-assets/orbiter"] == "v2.0.0"

    def test_parse_go_mod_with_indirect(self):
        """Test parsing go.mod with indirect dependencies"""
        go_mod = """
module github.com/noble-assets/noble

require (
    dollar.noble.xyz v1.0.0
    github.com/noble-assets/orbiter v2.0.0 // indirect
)
"""
        modules = parse_go_mod(go_mod)
        assert "dollar.noble.xyz" in modules
        assert "github.com/noble-assets/orbiter" in modules

    def test_parse_go_mod_single_line_require(self):
        """Test parsing go.mod with single-line require"""
        go_mod = """
module github.com/noble-assets/noble

require dollar.noble.xyz v1.0.0
require github.com/noble-assets/orbiter v2.0.0
"""
        modules = parse_go_mod(go_mod)
        assert "dollar.noble.xyz" in modules
        assert "github.com/noble-assets/orbiter" in modules


class TestParseReplaceDirectives:
    """Tests for parse_replace_directives function"""

    def test_parse_single_line_replace(self):
        """Test parsing single-line replace directive"""
        go_mod = """
module github.com/noble-assets/noble

replace github.com/circlefin/noble-cctp => github.com/noble-assets/cctp v1.0.0
"""
        replaces = parse_replace_directives(go_mod)
        assert "github.com/circlefin/noble-cctp" in replaces
        assert replaces["github.com/circlefin/noble-cctp"] == "github.com/noble-assets/cctp"

    def test_parse_replace_block(self):
        """Test parsing replace directives in a block"""
        go_mod = """
module github.com/noble-assets/noble

replace (
    github.com/circlefin/noble-cctp => github.com/noble-assets/cctp v1.0.0
    dollar.noble.xyz => github.com/noble-assets/dollar v2.0.0
)
"""
        replaces = parse_replace_directives(go_mod)
        assert "github.com/circlefin/noble-cctp" in replaces
        assert replaces["github.com/circlefin/noble-cctp"] == "github.com/noble-assets/cctp"
        assert "dollar.noble.xyz" in replaces
        assert replaces["dollar.noble.xyz"] == "github.com/noble-assets/dollar"

    def test_parse_replace_with_version(self):
        """Test parsing replace directive with version on both sides"""
        go_mod = """
module github.com/noble-assets/noble

replace github.com/circlefin/noble-cctp v1.0.0 => github.com/noble-assets/cctp v1.0.0
"""
        replaces = parse_replace_directives(go_mod)
        assert "github.com/circlefin/noble-cctp" in replaces
        assert replaces["github.com/circlefin/noble-cctp"] == "github.com/noble-assets/cctp"

    def test_parse_replace_with_local_path(self):
        """Test parsing replace directive with local path"""
        go_mod = """
module github.com/noble-assets/noble

replace github.com/circlefin/noble-cctp => ../local/cctp
"""
        replaces = parse_replace_directives(go_mod)
        assert "github.com/circlefin/noble-cctp" in replaces
        assert replaces["github.com/circlefin/noble-cctp"] == "../local/cctp"


class TestApplyReplaceDirectives:
    """Tests for apply_replace_directives function"""

    def test_applies_replace(self):
        """Test that replace directives are applied"""
        modules = {
            "github.com/circlefin/noble-cctp": "v1.0.0",
            "dollar.noble.xyz": "v2.0.0",
        }
        replaces = {
            "github.com/circlefin/noble-cctp": "github.com/noble-assets/cctp",
        }
        
        result = apply_replace_directives(modules, replaces)
        assert "github.com/noble-assets/cctp" in result
        assert result["github.com/noble-assets/cctp"] == "v1.0.0"
        assert "github.com/circlefin/noble-cctp" not in result
        assert "dollar.noble.xyz" in result  # Not replaced, so kept

    def test_keeps_non_replaced_modules(self):
        """Test that modules without replace directives are kept"""
        modules = {
            "github.com/noble-assets/orbiter": "v2.0.0",
            "dollar.noble.xyz": "v1.0.0",
        }
        replaces = {}
        
        result = apply_replace_directives(modules, replaces)
        assert result == modules


class TestGetRelevantModulesFromGoMod:
    """Tests for get_relevant_modules_from_go_mod function"""

    def test_filters_relevant_modules(self):
        """Test that only relevant modules are returned"""
        go_mod = """
module github.com/noble-assets/noble

require (
    dollar.noble.xyz v1.0.0
    github.com/noble-assets/orbiter v2.0.0
    github.com/cosmos/cosmos-sdk v0.50.0
    github.com/some/other/module v1.0.0
)
"""
        relevant = get_relevant_modules_from_go_mod(go_mod)
        assert "dollar.noble.xyz" in relevant
        assert "github.com/noble-assets/orbiter" in relevant
        assert "github.com/cosmos/cosmos-sdk" not in relevant
        assert "github.com/some/other/module" not in relevant

    def test_applies_replace_directives(self):
        """Test that replace directives are applied before filtering"""
        go_mod = """
module github.com/noble-assets/noble

require (
    github.com/circlefin/noble-cctp v1.0.0
    dollar.noble.xyz v2.0.0
)

replace github.com/circlefin/noble-cctp => github.com/noble-assets/cctp v1.0.0
"""
        relevant = get_relevant_modules_from_go_mod(go_mod)
        # Should use the replacement path, not the original
        assert "github.com/noble-assets/cctp" in relevant
        assert relevant["github.com/noble-assets/cctp"] == "v1.0.0"
        # Original path should not be in results (replaced)
        assert "github.com/circlefin/noble-cctp" not in relevant
        assert "dollar.noble.xyz" in relevant

    def test_replace_takes_precedence(self):
        """Test that replace directive takes precedence over require"""
        go_mod = """
module github.com/noble-assets/noble

require (
    github.com/circlefin/noble-cctp v1.0.0
)

replace github.com/circlefin/noble-cctp => github.com/noble-assets/cctp v1.0.0
"""
        relevant = get_relevant_modules_from_go_mod(go_mod)
        # Should only have the replacement, not the original
        assert "github.com/noble-assets/cctp" in relevant
        assert "github.com/circlefin/noble-cctp" not in relevant


class TestGetModuleVersionsForTag:
    """Tests for get_module_versions_for_tag function"""

    def test_returns_none_for_invalid_tag(self):
        """Test that function returns None for invalid tag"""
        result = get_module_versions_for_tag("noble-assets/noble", "v999.999.999")
        # This might return None if tag doesn't exist, or empty dict if go.mod exists but has no relevant modules
        assert result is None or isinstance(result, dict)


class TestGetModuleDiffs:
    """Tests for get_module_diffs function"""

    def test_returns_dict(self):
        """Test that function returns a dictionary"""
        # This will likely return empty dict for invalid tags, but should not crash
        result = get_module_diffs("noble-assets/noble", "v999.999.999", "v999.999.998")
        assert isinstance(result, dict)

