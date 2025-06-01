#!/usr/bin/env python3
"""Defines a module to test utils file"""
from utils import access_nested_map
import unittest
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """Defines test case methods to test that the methods
    in utils returns what its supposed to"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that the method returns what it is supposed to"""
        self.assertEqual(access_nested_map(nested_map=nested_map, path=path),
                         expected)
        
    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """Test that a KeyError is raised for the respective inputs"""
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
        self.assertEqual(f"KeyError('{expected}')", repr(e.exception))


if __name__ == "__main__":
    unittest.main()
