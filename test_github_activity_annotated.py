"""
Test Suite for GitHub Activity CLI Tool

This module contains unit tests for the GitHub Activity CLI tool,
testing both successful and error cases for username parsing and
GitHub API interactions.

Author: Coleman Grustas
Date: 12/28/24
"""


from github_activity_annotated import get_username, get_user_activities
import io
import json
import unittest
import unittest.mock

"""

"""

# region: Additional Features
    # Consider adding a test for when an empty string is passed as the username
# endregion

# region: How to inherit a parent class?
# the class within the parentheses is the parent class
# endregion:
# region: What is a TestCase? 
    # a TestCase provides access to:
    #  - assertion methods (test functions)
    #  - test fixtures (methods that run before/after tests to set up/tear down test data)
    # It also can automatically find and run tests. Any method that starts with test_ is considered a test. 
# endregion:
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
    test_get_user_activities_success()
        Tests successful GitHub API interaction
    test_get_user_activities_error()
        Tests error handling for failed API requests
    """
    # TODO: add a docstring to the test class itself to describe what it's testing
    def setUp(self): 
        """
        Set up test fixtures before each test method.

        Creates a sample GitHub API response structure containing
        three different types of events (Push, Issues, Watch) that
        will be used to verify API response handling.
        """
        # region: How did you choose the three specific events for the events data stub?
            # I included three different event types (PushEvent, IssuesEvent, WatchEvent), because they correspond to the example output
        # endregion:
        # region: Why include the "payload" attribute for the events data stub?
            # For the PushEvent, "payload" allows us to know how many commits were pushed, satisfying the
            #  "Pushed 3 commits to..." requirement of the sample output
            
            # For the IssuesEvent, "payload" allows us to see the action made to the issue, satisfying the 
            # "Opened a new issue in..." requirement
        # endregion:
        self.sample_events_data = [
            # region: What is a PushEvent?
                # A PushEvent represents when commits (code changes) are pushed (sent) to a repository.
                # Pushes usually include any updates (adding files, deleting files, modifying existing files) that you may make. 
                # They include information about: 
                    # The repository that received the push
                    # The branch that was pushed to
                    # Details about the commits that were made
                    # etc.
            # endregion:
            {
                "type" : "PushEvent",
                "repo" : {
                    "name": "kamranahmedse/developer-roadmap"
                },
                # region: What is a payload? 
                    # a payload is a JSON containing a boatload of data about the GitHub event, including: 
                        # What specific changes were made
                        # Timestamps of when the data occurred
                        # Who initiated the action
                        # Which repository was affected
                        # Related metadata about the event 
                        # etc. 
                # endregion:
                "payload" : {
                    "commits" : [
                        {"message": "first commit"},
                        {"message": "second commit"},
                        {"message": "third commit"}
                    ]
                }
            },

            # region: What is an IssuesEvent?
                # An IssuesEvent occurs whenever an issue is uploaded/updated to/in a respository
                # An issue is a GitHub feature for programmers to manage tasks, report bugs, and 
                # communicate ideas (like suggesting features) to one another. 
            # endregion:
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

            # region: What is a WatchEvent? What does it mean to 'star' a repository? 
                # A WatchEvent occurs when someone stars a repository. Starring a repository is GitHub's version of 'liking'
                # or 'bookmarking' a project. If you come across a useful/interesting project,
                # starring the repository makes it easy to access later, and it also helps signal a marker of quality to other programmers. 
                # If you see a project with lots of stars, you can tell that it's highly trusted/used by the devloper community. 
            # endregion:
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
        # region: Why hard code the command line arguments in a list?
            # I hard coded the command line arguments in a list because that is what 
        # endregion:
        test_args = ['script.py', 'testuser'] 

        # region: What is a "with" statement in Python? What is the difference between "with" and "with ___ as ___"?
            # a "with" statement is a context manager that creates a scope to manage (open/close) commmon resources (other context managers)
            # In this case, "with" opens/closes the replacement of sys.argv with test_args for testing purposes.
        # endregion:
        # region: What is a context manager? 
            # A context manager automatically handles the setup/cleanup of a resource. 
        # endregion:
        # region: What is a resource? 
            # A resource is anything that needs to be required, managed, and released, such as: 
                # System Resources (opening files, allocating memory, connecting datatbases, etc.)
                # Hardware Resources
                # Software/Programming Resources (test environments (like patch() in this case), cache contexts, database transactions, etc.)
        # endregion:
        # region: What is unittest.mock?
            # unittest.mock is a library that allows you to replace certain tests in your system under test with mock (simplified) objects, 
            # also known as stubs.
            # You can make assertions (write tests) about how they have been used. 
            # In this case, we are hard coding the command line arguments so that we can test whether the username was properly retreived.
        # endregion:
        # region: What is patch()? 
            # Temporarily replaces real objects (target) with a mock object (new) during testing
            # In this case, we're replacing 'sys.argv' with 'test_args' so that we don't have to manually 
            # read from the command line when testing
        # endregion:
        # region: What is a decorator? 
            # decorator : Function | Class -> Function | Class
            # Interpretation: Takes in a function, and returns an extended/modified version the function or class
        # endregion:
        # region: Why use sys in the test if we don't use it in the github_activity_annotated.py? 
            # We actually do call sys indirectly through argparse in the main code. When we call parser.parse_args(), it reads
            # from sys.argv[1:] to access the actual arguments, and place them in a Namespace(username='<whatever_username_was_input>')
        # endregion
        # region: What is sys.argv? 
            # sys.argv is a List of the command line arguments
        # endregion
        with unittest.mock.patch('sys.argv', test_args):        
            result = get_username()
            test_username = test_args[1]
            self.assertEqual(result, test_username)


    def test_get_username_no_args(self): 
        """Test handling of missing command line arguments"""
        test_args = ['script.py']  # Only program name, no username
        with unittest.mock.patch('sys.argv', test_args):
            # region: What is this code doing? 
                # The desired behavior for get_username() in this case is to raise a SystemExit (request to exit from the interpreter)
                # assertRaises(SystemExit) passes if a SystemExit is raised. It fails if any other exception 
                # (or no exception at all) is raised. 
                # Should raise SystemExit because argparse will exit when required args are missing
            # endregion
            # region: What are assertRaises? How is assertRaises (sometimes) used as a context manager? 
                # assertRaises are used to check if an exception is raised by a function or not (which allows us to test for invalid inputs)
                # assertRaises raises an ExceptionError if the desired exception is not raised

                # assertRaises can be used as a context manager, because it: 
                    # 'enters' the exception catching scaffold
                    # runs the code
                    # checks if the right exception was raised
                    # 'exits' the scaffold
            # endregion
            # region: What is a SystemExit? 
            with self.assertRaises(SystemExit):
                get_username() 

        

    # TODO: Write successful test for get_user_activities()
    def test_get_user_activities_success(self): 
        """Test successful GitHub API interaction and response parsing"""
        username = "testuser"
        
        # Create a mock HTTPResponse
        # region: TODO: What is UTF-8? 
            # UTF-8 (Unicode Transformation Format - 8-bit) is a commonly used Unicode character set 
            # that defines how characters are turned into bytes
            # We use UTF-8 here because it's the most common encoding on the web, and consequently, 
            # GitHub's API returns data in UTF-8 encoding
        # endregion
        # region: TODO: What is encode()? 
            # encode : String -> Bytes (raw binary data)
            # translates human readable text into computer-readable data
        # endregion
        # region: What is the return_value attribute in Mock objects? 
            # return_value is a built in attribute of every Mock that sets the return value when calling the mock object
            # In this case, we use return_value to set the value of our mock_response.read() to the byte
            # format of our sample_events_data
            # We do this so that we don't have to make a request to GitHub every time we want to test our function
        # endregion
        mock_response = unittest.mock.Mock()
        data_as_json_str = json.dumps(self.sample_events_data)
        data_as_bytes = data_as_json_str.encode('utf-8')
        mock_response.read.return_value = data_as_bytes

        # Mock the urlopen function to return our mock response
        # region: Why does setting 'mock_urlopen.__enter__' work if 'with' calls __enter__ immediately?
            # 'with' statements typically call __enter__ immediately upon entering the block. 
            # However, "with" statements treat unittest.mock.patch() objects differently. 
            # This is because the mock object is just a replacement behavior, not a real resource that needs managing. 

            # With mock.patch() objects, '__enter__' is not called until the code under test uses 
            # 'urllib.request.urlopen' under a with statement
            # So when we use '...as mock_urlopen', the mock is set up, but '__enter__' is not called,
            # because the replacement has not yet not occured. 

            # Therefore, we can configure '__enter__' to set up what will happen WHEN enter is called, not
            # after it's called. 
            
            # In this case, when __enter__ is called in 'get_user_activities', it will receive 'mock_response'. 

        # endregion
        # region: If the mock.patch() does not manage memory, why does it need to be placed in a "with" block? 
            # Regular 'with' is about resource management (open/close files, lock/unlock resources)
            # mock.patch 'with' is about scope management
            # We use 'with' in this case to define where the mock replacement is active
        # endregion
        with unittest.mock.patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.return_value.__enter__.return_value = mock_response
            result = get_user_activities(username)
            
            # Verify the result is a list and matches our sample data
            self.assertIsInstance(result, list)
            self.assertEqual(result, self.sample_events_data)


    # TODO: Write failed test for get_user_activities()
    # This specifically tests our error handling code, and ensures that an Exception is raised
    def test_get_user_activities_error(self):
        """Test error handling for failed GitHub API requests"""
        username = "nonexistentuser"

        with unittest.mock.patch('urllib.request.urlopen') as mock_urlopen:
            # region: TODO: What is mock.side_effect? 
                # mock.side_effect lets you define what happens when the mock object occurs. It can: 
                    # Raise an Exception
                    # Return different values on successive calls
                    # Run a function (if the Mock is a function)
            # endregion
            mock_urlopen.side_effect = Exception("API Error")
            result = get_user_activities(username)

            self.assertIsInstance(result, str)
            # region: TODO: What is startswith()? 
                # startswith(prefix) -> Boolean
                # Returns True if a String starts with a specific prefix, False otherwise
            # endregion
            self.assertTrue(result.startswith("Error:"))

def test_display_user_activity_success(self):
    """Test that the user activity is displayed correctly"""
    # Arrange: Use the sample data already defined in setUp()
    expected_output = [
        "Pushed 3 commits to kamranahmedse/developer-roadmap",
        "Opened a new issue in kamranahmedse/developer-roadmap",
        "Starred kamranahmedse/developer-roadmap"
    ]

    # TODO: Act & Assert: Capture stdout and verify output
    # region: What is sys.stdout? 
        # sys.stdout is Python's standard output stream
        # An output stream is a sequence of data that carries data from one place to another, 
        # typically from your program to your terminal screen (print() -> sys.stdout -> Terminal).
        # In this case, we're using unittest.mock.patch to replace the sys.stdout to a StringIO buff
        # In this case, we're redirecting the stream (["Hello"] -> sys.stdout -> StringIO buffer)
    # endregion
    # region: What is io.StringIO? 
        # StringIO is an in-memory file-like object 
        # In this case, we use it to replace a file-like object for testing purposes
    # endregion
    # region: What is a file-like object? 
        # A file-like object supports file-like methods, such as: 
            # .read() (reading data, or opening the stream)
            # .write() (writing data)
            # .close() (closing the stream)
        # Examples of file-like objects: 
            # actual files
            # sys.stdout, sys.stdin, sys.stderr
            # io.StringIO, io.BytesIO (in-memory text/binary streams)
    # endregion
    with unittest.mock.patch('sys.stdout', new=io.StringIO()) as mock_stdout:
        display_user_activity(self.sample_events_data) # redirects output stream to mock_stdout

        # strip() removes whitespace, split() separates each event into list of substrings
        actual_output = mock_stdout.getvalue().strip().split('\n')
        self.assertEqual(actual_output, expected_output)

def test_display_user_activity_error(self):
    """Test handling of error response from API"""
    with unittest.mock.patch('sys.stdout', new=io.StringIO()) as mock_stdout:
        display_user_activity("invalidresponse") # redirects output stream to mock_stdout
        assertEqual(
            mock_stdout.getvalue().strip(),
            "Error: Unable to display GitHub activity"
        )






    

if __name__ == '__main__':
    unittest.main() # runs all tests just by running the file