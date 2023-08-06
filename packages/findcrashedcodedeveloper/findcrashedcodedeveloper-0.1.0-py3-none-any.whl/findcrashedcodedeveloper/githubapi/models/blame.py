from .user import GithubUser


class GithubBlame:
    """A class to store blame info for a file"""

    def __init__(self, blame_ranges):
        """
        Parameters
        ----------
        blame_ranges : list
            list of dict objects having following information.
            {
                'startingLine': int,
                'endingLine': int,
                'author': {
                    'name': str,
                    'email': str,
                    'username': str
                }
            }
        """
        self._ranges = blame_ranges

    def get_line_author_info(self, line_number):
        """Get author info of given line number

        Parameters
        ----------
        line_number : int
            Line number in the file, numbers start from 1.

        Returns
        -------
        GithubUser
            Line author information
        """
        for file_range in self._ranges:
            if file_range['startingLine'] <= line_number <= file_range['endingLine']:
                return GithubUser(
                    name=file_range['author']['name'],
                    email=file_range['author']['email'],
                    username=file_range['author']['username']
                )
