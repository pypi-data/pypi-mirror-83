# Support Python 2
from __future__ import print_function


def print_github_user(github_user, heading='Author:'):
    """Print Github user information

    Parameters
    ----------
    github_user : GithubUser
    heading : str
    """
    print(heading)
    print('Name:', github_user.get_name())
    print('UserName:', github_user.get_username())
    print('Email:', github_user.get_email())
