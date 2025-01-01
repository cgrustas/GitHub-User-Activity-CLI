# GitHub User Activity CLI

## Description
A command-line interface tool that fetches and displays a GitHub user's recent activity using the GitHub API. This CLI tool provides a streamlined way to monitor GitHub activity from any public user without leaving your terminal. 

### Technologies Used
This application is built in Python, using only built-in libraries to learn more about Python's standard library, and to keep the installation process simple for users. The libraries used include: 
- `argparse` for command-line argument parsing
- `urllib.request` for making requests to the GitHub API
- `json` for processing API responses
- `unittest` and `unittest.mock` for testing

### Future Enhancements
- Filter activity by event type (i.e. only show push events or issue events)
- Allow configuration of time range for activity fetching  
- Cache the fetched data to improve performance.
- Explore other endpoints of the GitHub API to fetch additional information about the user or their repositories.

## How to Install the Project
1. **Clone the repository**
```
git clone [repository-url]
cd github-activity-cli
```

2. **Set up GitHub Authentication**
- [Create a GitHub Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

- Store Token as an Environment Variable _(the following steps are for macOS)_
  - Open Terminal
  - Open your shell profile file using a text editor: `nano ~/.zshrc`
  - Add your Token using the export command: `export GITHUB_USER_ACTIVITY_CLI_TOKEN="your_token_here"`
  - Save the file: Press Ctrl + X, then Y to confirm, then Enter
  - Reload your profile: `source ~/.zshrc`
  - Verify that it worked: Type `env` in terminal, then look for the token

## How to Use the Project
Run the CLI tool by providing a GitHub username
```
python3 github_activity.py <username>
```

**Example Input/Output**
```
python3 github_activity.py cgrustas
```
```
Output:
- Pushed 1 commit to cgrustas/GitHub-User-Activity-CLI
- Pushed 2 commits to cgrustas/GitHub-User-Activity-CLI
- Created a Git branch in cgrustas/GitHub-User-Activity-CLI
- Created a Git repository in cgrustas/Number-Guessing-Game
- ...
```

## Credits
- The inspiration for this project idea and requirements came from [roadmap.sh](url): [GitHub User Activity](https://roadmap.sh/projects/github-user-activity)

**Additional Sources**
- [What is an API?](https://aws.amazon.com/what-is/api/)
- [What is a REST API?](https://www.redhat.com/en/topics/api/what-is-a-rest-api)
- [Documenting Python Code: A Complete Guide](https://realpython.com/documenting-python-code/)
- [Claude.ai](https://claude.ai/new)
- [GeeksforGeeks](https://www.geeksforgeeks.org/)
- [How to Write a Good README File for Your GitHub Project](https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/)
