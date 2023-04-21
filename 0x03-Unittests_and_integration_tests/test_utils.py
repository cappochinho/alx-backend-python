#!/usr/bin/env python3
"""
This module contains unittests for the
utils.py module in the parent directory
"""


import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    This class contains tests for the access_nested_map
    method of the utils.py module
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """
        Tests that the named method returns what
        it is supposed to
        """

        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test that a KeyError is raised given the parameters above
        """

        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    This class contains tests for the getjson method
    of the utils.py module
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """
        Tests that the method returns the expected result
        """

        with patch('requests.get') as mock_get:
            mock_result = Mock(return_value=test_payload)
            mock_get.return_value = Mock(json=mock_result)

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Memoization of the 'a_method'
    """

    class TestClass:

        def a_method(self):
            return 42

        @memoize
        def a_property(self):
            return self.a_method()

    @patch.object(TestClass, 'a_method')
    def test_memoize(self, mock_a_method):
        """Testing memoize"""

        instance = self.TestClass()

        result1 = instance.a_property
        result2 = instance.a_property

        mock_a_method.assert_called_once()

        self.assertEqual(result1, result2)


if __name__ == '__main__':
    unittest.main()
