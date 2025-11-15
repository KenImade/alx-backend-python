#!/usr/bin/env python3
"""
Unittests for the GithubOrgClient class in client.py
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


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

        with patch.object(GithubOrgClient, "_public_repos_url",
                          new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://example.com/repos"

            client = GithubOrgClient("test_org")
            repos = client.public_repos()

            # Check returned repo names
            expected_names = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected_names)

            # Check that _public_repos_url was accessed once
            mock_url.assert_called_once()

            # Check that get_json was called once with mocked URL
            mock_get_json.assert_called_once_with("http://example.com/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns correct boolean value"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up class fixtures before running tests"""

        def side_effect_function(url):
            """Side effect function to return appropriate
            payload based on URL
            """

            class MockResponse:
                """Mock response object"""

                def __init__(self, json_data):
                    self.json_data = json_data

                def json(self):
                    """Return json data"""
                    return self.json_data

            # Map URLs to their corresponding payloads
            if url == "https://api.github.com/orgs/google":
                return MockResponse(cls.org_payload)
            elif url == cls.org_payload.get("repos_url"):
                return MockResponse(cls.repos_payload)
            return MockResponse(None)

        # Start the patcher for requests.get
        cls.get_patcher = patch('requests.get',
                                side_effect=side_effect_function)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down class fixtures after running tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected results from fixtures"""
        client = GithubOrgClient("google")
        repos = client.public_repos()

        # Check that the returned repos match expected_repos from fixtures
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filter returns expected results"""
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")

        # Check that the returned repos match apache2_repos from fixtures
        self.assertEqual(repos, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
