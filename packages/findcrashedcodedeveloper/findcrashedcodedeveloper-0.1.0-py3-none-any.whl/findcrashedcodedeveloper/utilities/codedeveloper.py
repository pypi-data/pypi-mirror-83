from ..githubapi.models.exceptions import InvalidLineNumberException

from .filepath import (
    get_all_possible_repository_paths,
    get_all_possible_repository_root_directory_paths
)


def _find_crashed_code_author(github_api, repository, branch, filepath, trace_line):
    """If this file contains crashed line then author of that line is returned"""
    try:
        file = github_api.files.get_file_content(
            repository, filepath, branch=branch
        )

        line_number = trace_line.get_crashed_line_number()
        if file.get_line_code(line_number) != trace_line.get_crashed_line_code():
            return

        blame = github_api.blames.get_blame(
            repository, filepath, branch=branch
        )
        return blame.get_line_author_info(line_number)
    except (InvalidLineNumberException, FileNotFoundError):
        return None


def get_crashed_code_author(github_api, repositories_info, stack_trace):
    """Return author of crashed code

    Parameters
    ----------
    github_api : GithubAPI
    repositories_info : list of RepositoryInfo
        information about possible github repositories for which this
        crash can belong.
    stack_trace : SentryStackTrace
        stack trace of the crash

    Returns
    -------
    GithubUser
        author responsible for crash
    """
    repository_files = {}
    for trace_line in stack_trace.get_trace_lines():
        absolute_filepath = trace_line.get_absolute_filepath()

        for repository_info in repositories_info:
            repository = repository_info.repository
            branch = repository_info.branch
            repository_name = repository.repository_name

            # match by repository name
            possible_repository_paths = get_all_possible_repository_paths(
                absolute_filepath, repository_name
            )

            for path in possible_repository_paths:
                author = _find_crashed_code_author(
                    github_api, repository, branch, path, trace_line
                )
                if author:
                    return author

            # match by repository root files
            if repository_info not in repository_files:
                repository_files[repository_info] = github_api.files.get_files(
                    repository, '', branch=branch
                )

            possible_repository_paths = get_all_possible_repository_root_directory_paths(
                absolute_filepath, repository_files[repository_info]
            )

            for path in possible_repository_paths:
                author = _find_crashed_code_author(
                    github_api, repository, branch, path, trace_line
                )
                if author:
                    return author
