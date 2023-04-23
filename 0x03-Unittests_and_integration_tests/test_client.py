#!/usr/bin/env python3
"""
this module contains the test suite for
the client.py module
"""


import unittest
from unittest.mock import MagicMock, patch
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

    @patch("client.get_json")
    @patch.object(GithubOrgClient, "_public_repos_url", new_callable=MagicMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        mock_public_repos_url.return_value = "https://api.github.com/orgs/test_org/repos"
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "my_license"}},
            {"name": "repo2", "license": {"key": "other_license"}},
            {"name": "repo3"}
        ]

        client = GithubOrgClient("test_org")
        repos = client.public_repos("my_license")

        self.assertEqual(repos, ["repo1"])
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        [{"license": {"key": "my_license"}}, "my_license", True],
        [{"license": {"key": "other_license"}}, "my_license", False]
    ])
    def test_has_license(self, repo, license_key, expected_result):
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
