# Coleman Grustas
# 12/28/24
# GitHub User Activity CLI
# Use GitHub API to fetch user activity and display it in the terminal.

# TODO: add proper Signatures/Purpose Statements for functions
# 

import argparse
import json
import os # for the authentication token
import urllib.request

# region: Additional Notes
# GITHUB_USER_ACTIVITY_CLI_TOKEN: Expires 1/27/25
# Handle errors gracefully, such as invalid usernames or API failures.
# Constraints: Do not use any external libraries or frameworks to fetch the GitHub activity.
# endregion:

def main():
    # accept the GitHub username as an argument from the command line
    username = get_username()
    print(username)

    # fetch the user’s recent activity using the GitHub API
    user_activities = get_user_activities(username)
    print(user_activities) # stop and test function before continuing with the code 

    # TODO: display the GitHub API in the terminal
    

# get_username : Void -> String
def get_username():
    args = parse_arguments() 
    return args.username

# parse_arguments : Void -> Namespace(username='<whatever_username_was_input>')
# Interpretation: parses the arguments that are provided when running the CLI
# region: Namespace Learning Notes
# A Namespace is an object where each defined argument becomes an attribute. 
# Examples: 
    # Namespace(username='johndoe')
    # Namespace(username='johndoe', email='johndoe@example.com')
# Interpretation: parses the arguments that are provided when running the CLI
# endregion:
def parse_arguments():
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





# get_user_activities : String -> Dictionary(?)
# Takes in a github username, and fetches the user’s recent activity using the GitHub API
# Returns a JSON representation of events for a user
def get_user_activities(username):
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
    

# region: "if __name__ == "__main__":" Learning Notes
# We use 'if __name__ == "__main__":' so that when importing modules from a Python script, we can use the functions defined
# in the script without actually executing the code in the script. 
# When Python runs a file directly, it sets a special variable '__name__' to the value "__main__". When Python
# imports the same file to another script, '__name__' is set to the module's name instead.
# endregion:
if __name__ == "__main__":
    main()