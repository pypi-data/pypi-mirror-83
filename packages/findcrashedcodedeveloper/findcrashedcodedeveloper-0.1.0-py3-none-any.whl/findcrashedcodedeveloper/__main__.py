"""Get the author info of a line"""
# Support Python 2
from __future__ import print_function

import argparse

from .githubapi import GithubAPI
from .githubapi.models.repository import GithubRepository
from .sentryapi import SentryAPI
from .models.repository_info import RepositoryInfo
from .utilities.sentrystacktrace import get_sentry_stack_trace_for_issue
from .utilities.codedeveloper import get_crashed_code_author
from .utilities.files import find_line_author_and_code_info
from .viewer.author import print_github_user
from .viewer.stack_trace import print_sentry_stack_trace
from .constants import GITHUB_API_SERVER_URL, SENTRY_URL


def _check_sentry_project(value):
    if '/' not in value:
        msg = (
            'Invalid sentry project: {}. '.format(value),
            'Project should be in format "organization/project"'
        )
        raise argparse.ArgumentTypeError(msg)

    return value


def _check_github_repository(value):
    if value.count('/') < 2:
        msg = (
            'Invalid github repository: {}. '.format(value),
            'Repository should be in format "owner/repository_name/branch"'
        )
        raise argparse.ArgumentTypeError(msg)

    return value


def _create_repository_info(repository_info_str):
    owner, repo_name, branch = repository_info_str.split('/', 2)
    return RepositoryInfo(
        GithubRepository(owner, repo_name),
        branch
    )


def _print_sentry_issues(sentry_api, sentry_project):
    organization, project = sentry_project.split('/', 1)
    issues_list = sentry_api.issues.get_list(
        organization, project
    )
    print('Issues:')
    for issue in issues_list:
        print(issue.id, ':',  issue.title)


def _print_crashed_code_developer_info(
    sentry_api, github_api, repositories, issue_id
):
    repositories_info = []
    for repo in repositories:
        repositories_info.append(
            _create_repository_info(repo)
        )

    stack_trace = get_sentry_stack_trace_for_issue(sentry_api, issue_id)

    print_sentry_stack_trace(stack_trace)
    print('')

    author = get_crashed_code_author(
        github_api, repositories_info, stack_trace
    )

    if author:
        print_github_user(author, heading='Developer:')
    else:
        print('Not able to find developer')


def _print_line_author_info(github_api, repository, filepath, line_number, extra_lines):
    repository_info = _create_repository_info(repository)

    line_info = find_line_author_and_code_info(
        github_api, repository_info.repository, filepath, line_number,
        branch=repository_info.branch, extra_lines=extra_lines
    )

    print('Code:')
    for i, code in enumerate(line_info.get_line_surrounding_code(), line_number-extra_lines):
        if i != line_number:
            print(i, ':', code)
        else:
            # add * after line number of main line
            print('{}*:'.format(i), code)

    print('')
    line_author = line_info.get_line_author()
    print_github_user(line_author, heading='Developer:')


def _parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)

    sentry_parent_parser = argparse.ArgumentParser(add_help=False)
    sentry_parent_parser.add_argument(
        '-s', '--sentry-api-token', help='Sentry API token', required=True
    )
    github_parent_parser = argparse.ArgumentParser(add_help=False)
    github_parent_parser.add_argument(
        '-g', '--github-api-token', help='Github API token', required=True
    )

    subparsers = parser.add_subparsers(dest='command')

    sentry_issues_parser = subparsers.add_parser(
        'sentryissues', parents=[sentry_parent_parser], help='Get issues in sentry project'
    )
    developer_finder_parser = subparsers.add_parser(
        'finddeveloper',
        parents=[sentry_parent_parser, github_parent_parser],
        help='Get crashed code developer info'
    )
    code_developer_parser = subparsers.add_parser(
        'codedeveloper', parents=[github_parent_parser], help='Get code developer info'
    )

    # sentry_issues_parser
    sentry_issues_parser.add_argument(
        '-p', '--sentry-project',
        help='Sentry Project. format: "organization/project"',
        required=True,
        type=_check_sentry_project
    )

    # developer_finder_parser
    developer_finder_parser.add_argument(
        '-r', '--repositories',
        help='list of repositories to search from. repository format: "owner/repository_name/branch"',
        nargs='+',
        required=True,
        type=_check_github_repository
    )
    developer_finder_parser.add_argument(
        '--issue-id', help='Sentry issue id', required=True
    )

    # code_developer_parser
    code_developer_parser.add_argument(
        '-r', '--repository',
        help='repository format: "owner/repository_name/branch"',
        required=True,
        type=_check_github_repository
    )

    code_developer_parser.add_argument(
        '-f', '--filepath', help='filepath in repository', required=True
    )
    code_developer_parser.add_argument(
        '-l', '--line-number',
        help='line number in file, first line number is 0',
        required=True, type=int
    )
    code_developer_parser.add_argument(
        '-e', '--extra-lines',
        help='extra lines code to fetch before and after main line',
        type=int, default=3
    )

    return parser, parser.parse_args()


def main():
    """Print crashed code author info"""
    parser, args = _parse_arguments()

    # sentry_api
    if args.command in ('sentryissues', 'finddeveloper'):
        sentry_api_token = args.sentry_api_token
        sentry_api = SentryAPI(sentry_api_token, server=SENTRY_URL)
    else:
        sentry_api = None

    # github_api
    if args.command in ('finddeveloper', 'codedeveloper'):
        github_api_token = args.github_api_token
        github_api = GithubAPI(
            github_api_token, api_server_url=GITHUB_API_SERVER_URL
        )
    else:
        github_api = None

    # execute command
    if args.command == 'sentryissues':
        sentry_project = args.sentry_project
        _print_sentry_issues(sentry_api, sentry_project)
        return
    elif args.command == 'finddeveloper':
        repositories = args.repositories
        issue_id = args.issue_id

        _print_crashed_code_developer_info(
            sentry_api, github_api, repositories, issue_id
        )
    elif args.command == 'codedeveloper':
        repository = args.repository
        filepath = args.filepath
        line_number = args.line_number
        extra_lines = args.extra_lines
        _print_line_author_info(
            github_api, repository, filepath, line_number, extra_lines
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
