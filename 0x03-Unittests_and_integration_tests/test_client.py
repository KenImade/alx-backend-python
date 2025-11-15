#!/usr/bin/env python3
"""
Unittests for the GithubOrgClient class in client.py
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected values"""

        test_payload = {"key": "value"}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        # Check the return value
        self.assertEqual(result, test_payload)
        # Check get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL from org"""

        test_payload = {
            "repos_url": "https://api.github.com/orgs/test_org/repos"}

        client = GithubOrgClient("test_org")

        # Patch the org property to return the test payload
        with patch.object(GithubOrgClient, "org",
                          new_callable=property) as mock_org:
            mock_org.return_value = test_payload

            result = client._public_repos_url

            # Check that _public_repos_url returns the expected URL
            self.assertEqual(result, test_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns correct repo names"""

        test_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}},
        ]
        mock_get_json.return_value = test_payload

        client = GithubOrgClient("test_org")

        with patch.object(GithubOrgClient, "_public_repos_url",
                          new_callable=property) as mock_url:
            mock_url.return_value = "http://example.com/repos"

            repos = client.public_repos()

            # Check returned repo names
            expected_names = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected_names)

            # Check that _public_repos_url was accessed once
            self.assertEqual(mock_url.call_count, 1)

            # Check that get_json was called once with mocked URL
            mock_get_json.assert_called_once_with("http://example.com/repos")


if __name__ == "__main__":
    unittest.main()
