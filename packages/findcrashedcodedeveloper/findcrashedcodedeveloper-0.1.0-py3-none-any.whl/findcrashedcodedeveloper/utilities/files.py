from ..githubapi.models.line import LineInfo


def find_line_author_and_code_info(github_api, repository, filepath, line_number, branch='master', extra_lines=0):
    """Get information about the line in file

    Parameters
    ----------
    github_api : GithubAPI
        GithubAPI object for making calls to Github APIs
    repository : GithubRepository
            repository object
    filepath : str
        unix style path of file inside the repository.
        example:- findthedeveloper/utilities/files.py
    line_number : int
        Number of line, number starts from 1
    branch : str, optional
        name of branch (default is 'master')
    extra_lines : int, optional
        extra lines to return before or after line_number line.
        extra_lines=3 mean 3 lines before & 3 lines after
        current line, Hence total 7 lines will be returned (default is 0).

    Returns
    -------
    LineInfo
        Information about the line
    """
    blame_info = github_api.blames.get_blame(
        repository, filepath, branch=branch
    )
    file_info = github_api.files.get_file_content(
        repository, filepath, branch=branch
    )

    start_line = line_number - extra_lines
    end_line = line_number + extra_lines

    lines_code = file_info.get_line_range_code(start_line, end_line)

    return LineInfo(
        lines_code=lines_code,
        line_author=blame_info.get_line_author_info(line_number)
    )