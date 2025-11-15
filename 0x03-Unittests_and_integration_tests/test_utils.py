#!/usr/bin/env python3
"""
Tests for the utils.py file
"""
from parameterized import parameterized
from typing import Mapping, Sequence, Any
from utils import access_nested_map
import unittest

class TestAccessNestedMap(unittest.TestCase):
    """Unit test for accessing nested map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence, expected: Any) -> None:
        """Ensures that accessing nested map returns the expected value"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

if __name__ == "__main__":
    unittest.main()
