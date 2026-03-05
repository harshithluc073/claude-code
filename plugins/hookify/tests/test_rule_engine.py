import sys
import os
import unittest

# Add plugins directory to sys.path so we can import hookify
current_dir = os.path.dirname(os.path.abspath(__file__))
plugin_root = os.path.dirname(current_dir)
plugins_dir = os.path.dirname(plugin_root)
if plugins_dir not in sys.path:
    sys.path.insert(0, plugins_dir)

from hookify.core.rule_engine import RuleEngine

class TestRuleEngine(unittest.TestCase):
    def setUp(self):
        self.engine = RuleEngine()

    def test_matches_tool_wildcard(self):
        """Test wildcard matcher '*' matches any tool."""
        self.assertTrue(self.engine._matches_tool('*', 'Bash'))
        self.assertTrue(self.engine._matches_tool('*', 'Edit'))
        self.assertTrue(self.engine._matches_tool('*', 'UnknownTool'))
        self.assertTrue(self.engine._matches_tool('*', ''))

    def test_matches_tool_exact_match(self):
        """Test exact matching of tool names."""
        self.assertTrue(self.engine._matches_tool('Bash', 'Bash'))
        self.assertFalse(self.engine._matches_tool('Bash', 'Edit'))

        # Test exact match isn't partial match
        self.assertFalse(self.engine._matches_tool('Bash', 'BashCommand'))
        self.assertFalse(self.engine._matches_tool('Bash', 'MyBash'))

    def test_matches_tool_or_pattern(self):
        """Test OR matching using '|'."""
        self.assertTrue(self.engine._matches_tool('Edit|Write', 'Edit'))
        self.assertTrue(self.engine._matches_tool('Edit|Write', 'Write'))
        self.assertFalse(self.engine._matches_tool('Edit|Write', 'Bash'))

        # Multiple ORs
        self.assertTrue(self.engine._matches_tool('Bash|Edit|Write', 'Write'))
        self.assertTrue(self.engine._matches_tool('Bash|Edit|Write', 'Bash'))
        self.assertFalse(self.engine._matches_tool('Bash|Edit|Write', 'MultiEdit'))

    def test_matches_tool_edge_cases(self):
        """Test edge cases with empty strings and whitespaces."""
        # Empty matcher should not match unless tool is empty
        self.assertTrue(self.engine._matches_tool('', ''))
        self.assertFalse(self.engine._matches_tool('', 'Bash'))

        # White spaces are treated literally by the current implementation
        self.assertTrue(self.engine._matches_tool('Bash| Edit', ' Edit'))
        self.assertFalse(self.engine._matches_tool('Bash| Edit', 'Edit'))

        self.assertFalse(self.engine._matches_tool('Bash ', 'Bash'))

        # Empty pattern in split "Bash|" -> ["Bash", ""]
        self.assertTrue(self.engine._matches_tool('Bash|', ''))
        self.assertTrue(self.engine._matches_tool('Bash|', 'Bash'))
        self.assertFalse(self.engine._matches_tool('Bash|', 'Edit'))

        self.assertTrue(self.engine._matches_tool('|Bash', ''))
        self.assertTrue(self.engine._matches_tool('||', ''))

if __name__ == '__main__':
    unittest.main()
