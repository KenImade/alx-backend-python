#!/usr/bin/env python3
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


if __name__ == "__main__":
    unittest.main()
