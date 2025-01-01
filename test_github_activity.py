"""
Test Suite for GitHub Activity CLI Tool

Author: Coleman Grustas
Date: 1/1/25
"""

from github_activity_annotated import get_username, get_user_activity, display_user_activity
import io
import json
import unittest
import unittest.mock


class TestGitHubActivityCLI(unittest.TestCase):
    """
    A test suite used to verify the GitHub Activity CLI functionality.

    Attributes
    ----------
    sample_events_data : list
        Mock GitHub API response containing three events:
        - A PushEvent with 3 commits
        - An IssuesEvent for a new issue
        - A WatchEvent for repository starring
        Used as test fixture across multiple test methods

    Methods
    -------
    setUp()
        Initializes test fixtures before each test method
    test_get_username_valid()
        Tests successful username extraction from command line
    test_get_username_no_args()
        Tests handling of missing command line arguments
    test_get_user_activity_success()
        Tests successful GitHub API interaction
    test_get_user_activity_error()
        Tests error handling for failed API requests
    """
    def setUp(self): 
        """Set up test fixtures before each test method"""
        self.sample_events_data = [
            {
                "type" : "PushEvent",
                "repo" : {
                    "name": "kamranahmedse/developer-roadmap"
                },
                "payload" : {
                    "commits" : [
                        {"message": "first commit"},
                        {"message": "second commit"},
                        {"message": "third commit"}
                    ]
                }
            },
            {
                "type": "IssuesEvent",
                "repo": {
                    "name": "kamranahmedse/developer-roadmap"
                },
                "payload": {
                    "action": "opened",
                    "issue": {
                        "title": "Sample issue title"
                    }
                }
            },
            {
                "type": "WatchEvent",
                "repo": {
                    "name": "kamranahmedse/developer-roadmap"
                },
                "payload": {
                    "action": "started"
                }
            }
        ]

    def test_get_username_valid(self):
        """Test successful username extraction from command line arguments"""
        test_args = ['script.py', 'testuser'] 
        with unittest.mock.patch('sys.argv', test_args):        
            result = get_username()
            test_username = test_args[1]
            self.assertEqual(result, test_username)


    def test_get_username_no_args(self): 
        """Test handling of missing command line arguments"""
        test_args = ['script.py']  # Only program name, no username
        with unittest.mock.patch('sys.argv', test_args):
            with self.assertRaises(SystemExit):
                get_username() 

    def test_get_user_activity_success(self): 
        """Test successful GitHub API interaction and response parsing"""
        username = "testuser"
        mock_response = unittest.mock.Mock()
        data_as_json_str = json.dumps(self.sample_events_data)
        data_as_bytes = data_as_json_str.encode('utf-8')
        mock_response.read.return_value = data_as_bytes

        # Mock the urlopen function to return our mock response
        with unittest.mock.patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.return_value.__enter__.return_value = mock_response
            result = get_user_activity(username)
            
            # Verify the result is a list and matches our sample data
            self.assertIsInstance(result, list)
            self.assertEqual(result, self.sample_events_data)

    def test_get_user_activity_error(self):
        """Test error handling for failed GitHub API requests"""
        username = "nonexistentuser"

        with unittest.mock.patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.side_effect = Exception("API Error")
            result = get_user_activity(username)

            self.assertIsInstance(result, str)
            self.assertTrue(result.startswith("Error:"))

def test_display_user_activity_success(self):
    """Test that the user activity is displayed correctly"""
    expected_output = [
        " - Pushed 3 commits to kamranahmedse/developer-roadmap",
        " - Opened a new issue in kamranahmedse/developer-roadmap",
        " - Starred kamranahmedse/developer-roadmap"
    ]

    # Capture stdout and verify output
    with unittest.mock.patch('sys.stdout', new=io.StringIO()) as mock_stdout:
        display_user_activity(self.sample_events_data) 
        actual_output = mock_stdout.getvalue().strip().split('\n')
        self.assertEqual(actual_output, expected_output)

def test_display_user_activity_error(self):
    """Test handling of error response from API"""
    with unittest.mock.patch('sys.stdout', new=io.StringIO()) as mock_stdout:
        display_user_activity("invalidresponse") 
        self.assertEqual(
            mock_stdout.getvalue().strip(),
            "Error: Unable to display GitHub activity"
        )

if __name__ == '__main__':
    unittest.main() 