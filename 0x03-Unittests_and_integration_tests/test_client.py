#!/usr/bin/env python3
"""
this module contains the test suite for
the client.py module
"""


import unittest
from unittest.mock import MagicMock, patch
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


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
    def test_public_repos(self, mock_get_json):
        mock_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache"}},
            {"name": "repo3", "license": None},
        ]
        mock_get_json.return_value = mock_payload

        client = GithubOrgClient("test_org")
        p_url = "_public_repos_url"

        with patch.object(client, p_url, new_callable=MagicMock) as m_p_url:
            m_p_url.return_value = "https://api.github.com/orgs/test_org/repos"
            mock_has_license = MagicMock(return_value=True)

            with patch.object(client, "has_license", mock_has_license):
                result = client.public_repos("mit")

                self.assertEqual(result, ["repo1"])
                m_p_url.assert_called_once()
                mock_has_license.assert_called_with(mock_payload[0], "mit")

    @parameterized.expand([
        [{"license": {"key": "my_license"}}, "my_license", True],
        [{"license": {"key": "other_license"}}, "my_license", False]
    ])
    def test_has_license(self, repo, license_key, expected_result):
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


class TestIntegrationGithubOrgClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = [
            org_payload,
            repos_payload,
        ]

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    @parameterized_class([
        {"license": None, "expected_repos": expected_repos},
        {"license": "apache-2.0", "expected_repos": apache2_repos},
    ])
    class TestPublicRepos(unittest.TestCase):

        def setUp(self):
            self.client = GithubOrgClient("test_org")

        def test_public_repos(self):
            repos = self.client.public_repos(license=self.license)
            self.assertEqual(repos, self.expected_repos)


if __name__ == "__main__":
    unittest.main()
