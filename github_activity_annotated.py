"""
GitHub User Activity CLI Tool

A command-line interface tool that fetches and displays GitHub user activity
using the GitHub API. This tool allows users to view recent GitHub events
for any specified username.

Author: Coleman Grustas
Date: 12/30/24

Project inspired by roadmap.sh's Python Projects
(https://roadmap.sh/projects/github-user-activity)

Environment Variables:
    GITHUB_USER_ACTIVITY_CLI_TOKEN (required): GitHub API authentication token
        Current token expires: 2025-01-27

Constraints: 
    - Do not use any external libraries or frameworks to fetch the GitHub activity.

Future Enhancements: 
    - Add error handling for empty string input in 'get_username()'
    - Filter the activity by event type.
    - Display the activity in a more structured format.
    - Cache the fetched data to improve performance.
    - Explore other endpoints of the GitHub API to fetch additional information about the user or their repositories.
"""

# region: TODO: What is an environment variable? 

import argparse
import json
import os # for the authentication token
import urllib.request

def main():
    """
    Main entry point for the GitHub Activity CLI tool.
    Gets the username, fetches activities, and displays results.
    """
    username = get_username()
    print(username)

    # fetch the user’s recent activity using the GitHub API
    user_activity = get_user_activity(username)

    # TODO(cgrustas): Display the fetched activity in the terminal
#    display_user_activity(user_activity)
    
def get_username():
    """
    Retrieves GitHub username from command line arguments.

    Returns:
        str: The GitHub username provided as a command line argument

    Raises:
        SystemExit: If no username is provided in command line arguments
    """
    args = parse_arguments() 
    return args.username

# Interpretation: parses the arguments that are provided when running the CLI
# region: Namespace Learning Notes
# A Namespace is an object where each defined argument becomes an attribute. 
# Examples: 
    # Namespace(username='johndoe')
    # Namespace(username='johndoe', email='johndoe@example.com')
# Interpretation: parses the arguments that are provided when running the CLI
# endregion:
def parse_arguments():
    """
    Sets up and parses command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments containing the username

    Raises:
        SystemExit: If required arguments are missing or invalid
    """
    # region: ArgumentParser Learning Notes
    # An ArgumentParser helps process command-line arguments
        # add_argument(), which tells the parser what to expect
        # parse_args(), which reads and processes the command-line inputs 
    # endregion:
    parser = argparse.ArgumentParser(
        description = 'A CLI tool to read in GitHub usernames'
    )

    # add argument for GitHub username
    # region: add_argument Learning Notes
    # add_argument() helps define how the command-line argument should be parsed
    # endregion:
    parser.add_argument(
        'username', # strings w/o dashes are treated as positional arguments
        type=str,
        help='GitHub username' # defines what the specific argument does
    )

    # parse the arguments
    # region: what isparse_args?
        # parse_args : ArgumentParser -> argparse.Namespace
        # extracts data from parser and places the attribute/value pairs into a Namespace
    # endregion:
    return parser.parse_args()

def get_user_activity(username):
    """
    Fetches recent GitHub activities for the specified user.

    Args:
        username (str): GitHub username to fetch activities for

    Returns:
        list[dict]: List of GitHub events if successful
        str: Error message if the request fails

    Note:
        Requires GITHUB_USER_ACTIVITY_CLI_TOKEN environment variable to be set
        for authentication.
    """
    # add path parameter to url
    url = f"https://api.github.com/users/{username}/events" 

    # Retrieve token from environment 
    token = os.environ.get('GITHUB_USER_ACTIVITY_CLI_TOKEN')

    # create request object to send out to server
    req = urllib.request.Request(
        url, # specifies which serve the request should go to
        headers = { 
            # region: "Accept" Header Learning Notes
            # specifies which response the client (this program) expects to receive
            # indicates to GitHub's server that I'd like to receive the response in GitHub's JSON format
            # endregion:
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}" 
        }
    )

    # open/parse the request
    try: 
        # region: urlopen Learning Notes
        # urlopen : Request -> HTTPResponse
        # endregion:
        # region: HTTPResponse Learning Notes
        # An HTTPResponse represents the response from an HTTP server after making a request.
        # It contains:
            # the content/data of the response (response body)
            # information about the respones (headers, status code)
            # methods to access the data (read())
            # 'with... as' means 'open this and call it response, and close/delete it when you're done'
        # endregion:
        with urllib.request.urlopen(req) as response: 
            # region: read() Learning Notes
                # read : HTTPResponse -> Raw Binary Dates
                # reads in data as bytes
            # endregion:
            data = response.read()

            # return a dictionary format of the json data
            # region: loads() Learning Notes
            # loads : String or Raw Binary Data containing JSON data -> Dictionary
            # takes in strings or bytes containing JSON data, and converts it to a Python Dictionary
            # endregion:
            return json.loads(data)
    # region: Exception Learning Notes
    # Exception is the base class for all built-in exceptions in Python
    # assigns the caught exception to an Exception object named e
    # str(e) converts the exception object to a string to show the error message
    # endregion:
    except Exception as e:    
        return f"Error: {str(e)}" 
    

    """
    Fetches recent GitHub activities for the specified user.

    Args:
        username (str): GitHub username to fetch activities for

    Returns:
        list[dict]: List of GitHub event dictionaries
        str: Error message if the request fails

    Note:
        Requires GITHUB_USER_ACTIVITY_CLI_TOKEN environment variable to be set
        for authentication.
    """

# TODO(cgrustas): Display the fetched activity in the terminal
#   - Format events based on type (PushEvent, IssuesEvent, etc.)
#   - Add color coding for different event types
#   - Include timestamp for each activity
#   - Handle pagination for users with many events
def display_user_activity(user_activity):
    """
    Displays the fetched activity in the terminal.

    Args: 
        user_activity (list[dict]): List of GitHub event dictionaries
    """
    pass

# region: "if __name__ == "__main__":" Learning Notes
# We use 'if __name__ == "__main__":' so that when importing modules from a Python script, we can use the functions defined
# in the script without actually executing the code in the script. 
# When Python runs a file directly, it sets a special variable '__name__' to the value "__main__". When Python
# imports the same file to another script, '__name__' is set to the module's name instead.
# endregion:
if __name__ == "__main__":
    main()