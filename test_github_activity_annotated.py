# Coleman Grustas
# 12/28/24

from github_activity_annotated import get_username
import json
import unittest
import unittest.mock

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
    # TODO: add a docstring to the test class itself to describe what it's testing
    def setUp(self): 
        """Create a stub for the GitHub user activity JSON data"""
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
        """Test get_username with valid username"""
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
        """Test get_username with no command line arguments"""
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
        """Test successful API response from get_user_activities"""
        username = "testuser"
        
        # Create a mock response object that behaves like an HTTP response
        # region: TODO: What is JSON.encode()? What is 'utf-8'? 
        # endregion
        # region: TODO: Why is return_value an attribute of read? Why is read an attribute of mock_response?

#        mock_response = unittest.mock.Mock()
#        data_in_json_str = json.dumps(self.sample_events_data)
#        data_in_bytes = data_in_json_str.encode('utf-8') # converts strings to bytes

        # region: TODO: What is the 'return_value' attribute in Mock objects? 
        # region: TODO: What is mock_response.read? Why is read an attribute of mock_response? 
        mock_response.read.return_value = json.dumps(self.sample_events_data).encode('utf-8')


    # TODO: Write failed test for get_user_activities()
    def test_get_user_activities_error(self):
        # probably use assertIsInstance(a, b) method in unittest framework
        pass


if __name__ == '__main__':
    unittest.main() # runs all tests just by running the file