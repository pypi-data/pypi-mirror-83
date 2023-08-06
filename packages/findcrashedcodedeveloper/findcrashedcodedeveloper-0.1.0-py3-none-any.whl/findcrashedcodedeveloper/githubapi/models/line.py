class LineInfo:
    """Class to represent a line code info"""

    def __init__(self, lines_code, line_author):
        """
        Parameters
        ----------
        lines_code : list of str
            List of str of lines codes.
            Middle line is the main line.
        line_author : GithubUser
            Author of main file
        """
        self._lines_code = lines_code
        self._line_author = line_author

    def get_line_author(self):
        """Get author of main line

        Returns
        -------
        GithubUser
            author of main line
        """
        return self._line_author

    def get_line_code(self):
        """Get main line code

        Returns
        -------
        str
            Main line code
        """
        line_index = len(self._lines_code) // 2
        return self._lines_code[line_index]

    def get_line_surrounding_code(self):
        """Get list of surrounding lines code

        Returns
        -------
        list of str
            List of str of lines code
        """
        return self._lines_code
