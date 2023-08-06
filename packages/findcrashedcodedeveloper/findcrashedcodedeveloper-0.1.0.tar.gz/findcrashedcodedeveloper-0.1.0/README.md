# Find The Developer

findcrashedcodedeveloper is python package which return the information about the developer who is responsible for code crash.

- It uses Github v4 graphql APIs for fetching the blame history of a file.
- It uses Sentry APIs to fetch stack trace of crash

## Installation

You can install it from [PyPI](https://pypi.org/project/findcrashedcodedeveloper/):

    pip install findcrashedcodedeveloper

The package is supported on Python 2.7, as well as Python 3.+.

## How to use

The findcrashedcodedeveloper has a command line application to demo some common functionality of this package. To see list of supported commands type `python -m findcrashedcodedeveloper -h`


Get latest issues from Sentry project:

    $ findcrashedcodedeveloper sentryissues -s <sentry_api_token> -p <sentry_user_name>/<sentry_project_name>

    $ findcrashedcodedeveloper sentryissues -s abcdefgh123 -p karambir252/testproject

    Issues:
    1964662080 : ZeroDivisionError: integer division or modulo by zero
    1864652080 : TypeError: Cannot convert undefined or null to object
    1754652310 : IndexError: index -1 is out of bounds for axis 0 with size 0

To get developer responsible for crashed code pass issue id:

    $ findcrashedcodedeveloper finddeveloper -s <sentry_api_token> --issue-id 1964662080 -g <github_api_token> -r <repo_owner_username>/<repo>/<branch>

    $ findcrashedcodedeveloper finddeveloper -s abcde1234 --issue-id 1964662080 -g abcde1234 -r karambir252/crashassigner/master

    Stack Trace:
    file: /home/karambir/myproject/project/crashassigner/src/tmp.py
    10:    c = b/a
    file: /home/karambir/myproject/project/crashassigner/src/tmp.py
    14:    main()

    Developer:
    Name: karambir252
    UserName: karambir252
    Email: <email>@gmail.com

You can also get developer of a line of code:

    $ findcrashedcodedeveloper codedeveloper -g <github_api_token> -r karambir252/findcrashedcodedeveloper/master --filepath README.md --line-number 30

    Code:
    17 : lib/
    18 : lib64/
    19 : parts/
    20*: sdist/
    21 : var/
    22 : wheels/
    23 : *.egg-info/

    Developer:
    Name: karambir252
    UserName: karambir252
    Email: <email>@gmail.com

