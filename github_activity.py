"""
GitHub User Activity CLI Tool

A command-line interface tool that fetches and displays GitHub user activity
using the GitHub API. This tool allows users to view recent GitHub events
for any public username.

Author: Coleman Grustas
Date: 1/1/25

Project inspired by roadmap.sh's Python Projects
(https://roadmap.sh/projects/github-user-activity)

Environment Variables:
    GITHUB_USER_ACTIVITY_CLI_TOKEN (required): GitHub API authentication token
        Current token expires: 2025-01-27

Constraints: 
    - Do not use any external libraries or frameworks to fetch the GitHub activity.

Future Enhancements: 
    - Filter the activity by event type.
    - Display the activity in a more structured format.
    - Cache the fetched data to improve performance.
    - Explore other endpoints of the GitHub API to fetch additional information about the user or their repositories.
"""

import argparse
import json
import os 
import urllib.request


def main():
    """
    Main entry point for the GitHub Activity CLI tool.
    Gets the username, fetches activities, and displays results.
    """
    username = get_username()
    user_activity = get_user_activity(username)
    display_user_activity(user_activity)
    
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

def parse_arguments():
    """
    Sets up and parses command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments containing the username

    Raises:
        SystemExit: If required arguments are missing or invalid
    """
    parser = argparse.ArgumentParser(
        description = 'A CLI tool to read in GitHub usernames'
    )

    parser.add_argument(
        'username', 
        type=str,
        help='GitHub username' 
    )
    
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
    url = f"https://api.github.com/users/{username}/events" 
    token = os.environ.get('GITHUB_USER_ACTIVITY_CLI_TOKEN')
    req = urllib.request.Request(
        url, 
        headers = { 
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}" 
        }
    )

    try: 
        with urllib.request.urlopen(req) as response: 
            data = response.read()
            return json.loads(data)
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

def display_user_activity(activities):
    """
    Displays the fetched activity in the terminal.

    Args: 
        activities (list[dict]): List of GitHub event Dictionaries
    """
    # handle invalid inputs
    if isinstance(activities, str) and activities.startswith("Error:"):
        print(activities)
        return    
    if not activities:
        print("No recent activity found.")
        return

    # print user activity
    print("Output:")
    for event in activities: 
        event_type = event["type"]
        repo_name = event["repo"]["name"]
        payload = event["payload"]
        action = payload["action"].capitalize() if "action" in payload else ""
        event_details = event_type

        if event_type == "CommitCommentEvent":
            event_details = f"{action} a commit comment"
        elif event_type == "CreateEvent": 
            event_details = f"Created a Git {payload["ref_type"]}"
        elif event_type == "DeleteEvent":
            event_details = f"Deleted a Git {payload["ref_type"]}"
        elif event_type == "ForkEvent":
            event_details = f"Forked a repository"
        elif event_type == "GollumEvent":
            event_details = f"{action} a wiki page"
        elif event_type == "IssueCommentEvent":
            event_details = f"{action} an issue comment"
        elif event_type == "IssuesEvent":
            event_details = f"{action} a new issue"
        elif event_type == "MemberEvent":
            if action == "Added":
                print(f"- Added member to {repo_name}") 
                continue # edge case, uses 'to' instead of 'in'
            elif action == "Edited":
                event_details = f"{action} changes to the collaborator permissions"
            else: 
                event_details = f"{action} MemberEvent"
        elif event_type == "PublicEvent":
            print(f"- Private repository {repo_name} is made public") 
            continue # another edge case
        elif event_type == "PullRequestEvent":
            event_details = f"{action} pull request #{payload["number"]}"
        elif event_type == "PullRequestReviewEvent":
            event_details = f"{action} pull request review"
        elif event_type == "PullRequestReviewCommentEvent":
            event_details = f"{action} pull request review comment"
        elif event_type == "PullRequestReviewThreadEvent":
            if action == "Resolved":
                event_details = f"{action} a comment thread on a pull request"
            elif action == "Unresolved":
                event_details = f"{action} a previously resolved comment thread on a pull request"
            else:
                event_details = f"There was a {event_type}"
        elif event_type == "PushEvent":
            if payload["size"] == 1: 
                print(f"- Pushed {payload["size"]} commit to {repo_name}")
            else:
                print(f"- Pushed {payload["size"]} commits to {repo_name}")
            continue
        elif event_type == "ReleaseEvent":
            event_details = f"{action} a release event"
        elif event_type == "SponsorshipEvent":
            event_details = f"{action} a sponsorship listing"
        elif event_type == "WatchEvent":
            if action == "Started":
                event_details = f"Starred"
            else:
                event_details = f"There was a {event_type}"
        else:
            event_details = f"There was a {event_type}"
        
        print(f"- {event_details} in {repo_name}")

if __name__ == "__main__":
    main()