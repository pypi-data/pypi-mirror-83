class SentryStackTraceLine:
    """A class to represent a single line in Sentry stack trace"""

    def __init__(
        self,
        absolute_filepath,
        crashed_line_number,
        crashed_line_code,
        crashed_line_context
    ):
        """
        Parameters
        ----------
        absolute_filepath : str
            absolute filepath of crashed file
        crashed_line_number : int
            line number of crashed line.
            line number starts from 1.
        crashed_line_code : int
            code at the crashed line
        crashed_line_context : list of dict
            code around the crashed line
            format of dict:
            {
                'lineNo': int,
                'code' : str
            }
        """
        self._absolute_filepath = absolute_filepath
        self._crashed_line_number = crashed_line_number
        self._crashed_line_code = crashed_line_code
        self._crashed_line_context = crashed_line_context

    def get_absolute_filepath(self):
        return self._absolute_filepath

    def get_crashed_line_number(self):
        """Get crashed code line number

        Returns
        -------
        int
            line number of crashed line.
            line number starts from 1.
        """
        return self._crashed_line_number

    def get_crashed_line_code(self):
        """Get code of crashed line

        Returns
        -------
        str
            code of crashed line
        """
        return self._crashed_line_code

    def iter_crashed_line_code(self):
        """Iterate on code around crashed line

        Yields
        ------
        line_number : int
            line number start from 1.
        code : str
            code at that line
        """
        for line_data in self._crashed_line_context:
            yield line_data['lineNo'], line_data['code']


class SentryStackTrace:
    """A class to represent the stack trace of crash in Sentry"""

    def __init__(self, trace_lines):
        """
        Parameters
        ----------
        trace_lines : list of SentryStackTraceLine
            list of SentryStackTraceLine for this crash.
            deepest line will be on top.
        """
        self._trace_lines = trace_lines

    def get_trace_lines(self):
        """Get lines in this stack trace

        Returns
        -------
        trace_lines : list of SentryStackTraceLine
            list of SentryStackTraceLine in this crash.
            deepest line will be on top.
        """
        return self._trace_lines
