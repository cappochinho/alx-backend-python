#!/usr/bin/env python3
"""
this module contains the test suite for
the client.py module
"""


import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Tests the class GithubOrgClient
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock):
        """tests the org method"""

        client = GithubOrgClient(org_name)
        client.org()
        mock.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch("client.get_json")
    def test_public_repos_url(self, mocked):
        """tests the public_repos_url method"""

        org_name = "test_org"
        repos_url = f"https://api.github.com/orgs/{org_name}/repos"
        mock_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mocked.return_value = mock_payload

        client = GithubOrgClient(org_name)
        result = client._public_repos_url

        self.assertEqual(result, repos_url)


if __name__ == "__main__":
    unittest.main()
