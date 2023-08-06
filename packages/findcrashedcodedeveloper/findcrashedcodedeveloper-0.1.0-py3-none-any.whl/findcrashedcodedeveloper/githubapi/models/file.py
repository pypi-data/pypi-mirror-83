from .exceptions import InvalidLineNumberException


class FileContent:
    """A class used to store content of a file"""

    def __init__(self, content):
        """
        Parameters
        ----------
        content : str
            content of the file
        """
        self._lines = content.splitlines()

    def get_line_code(self, line_number):
        """Get code of a line

        Parameters
        ----------
        line_number : str
            Number of line in file, numbering start from 1.

        Returns
        -------
        str
            Code at that line

        Raises
        ------
        InvalidLineNumberException
            If line number not exists in file
        """
        if line_number <= 0 or line_number > len(self._lines):
            raise InvalidLineNumberException(line_number)
        return self._lines[line_number-1]

    def get_line_range_code(self, start_line, end_line):
        """Get list of [start_line, end_line] code

        Parameters
        ----------
        start_line : int
            first line of range
        end_line : int
            last line of range

        Returns
        -------
        list
            list of str of code
        """
        if start_line <= 0 or start_line > len(self._lines):
            raise InvalidLineNumberException(
                start_line, line_label='start_line'
            )
        elif end_line <= 0 or end_line > len(self._lines):
            raise InvalidLineNumberException(end_line, line_label='end_line')
        elif end_line < start_line:
            raise InvalidLineNumberException(end_line, line_label='end_line')

        return list(self._lines[start_line-1: end_line])

    def get_number_of_lines(self):
        """Get number of lines in the file"""
        return len(self._lines)


class FileInfo:
    """Class to represent information about in file in repository"""

    def __init__(self, name, filepath, is_directory):
        """
        Parameters
        ----------
        name : str
            name of file
        filepath : str
            unix style path of file in repository
        is_directory : bool
            is this file a directory
        """
        self._name = name
        self._filepath = filepath
        self._is_directory = is_directory

    def get_name(self):
        """Get name of file"""
        return self._name

    def get_filepath(self):
        """Get repository path of file"""
        return self._filepath

    def is_directory(self):
        """Is this a directory"""
        return self._is_directory
